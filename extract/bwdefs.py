"""BigWorld/NeoX entity-def toolkit for the RoS private server.

Uses the named entities.npk dump (extract/entities_out + entities_names.json, names from the
cracked NPK hash in npk_hash.py) to:
  * resolve an entity's full property list in parse order
    (Parent first, then <Implements> recursively in listed order, then own <Properties>),
  * resolve alias types from alias.xml,
  * serialize default values for a createBasePlayer stream (BASE_AND_CLIENT properties).

Order rule confirmed on the live client with Account (iProxy props, then isMobileAccount).
"""
import json, os, pickle, re, struct

HERE = os.path.dirname(os.path.abspath(__file__))
BS = chr(92)


def _strip(t):
    return re.sub(r'<!--.*?-->', '', t, flags=re.S)


class Defs:
    def __init__(self, root=HERE):
        names = json.load(open(os.path.join(root, 'entities_names.json')))
        self.files = {}
        for fn, path in names.items():
            if path:
                self.files[path] = os.path.join(root, 'entities_out', fn)
        alias_fn = [fn for fn in os.listdir(os.path.join(root, 'entities_out')) if fn.startswith('640_')][0]
        self.alias_src = _strip(open(os.path.join(root, 'entities_out', alias_fn), 'rb').read().decode('utf-8', 'replace'))
        self._alias = {}
        self.defaults = {}          # prop name -> raw <Default> text (last definition wins)
        self._parse_alias()

    # ---------- files ----------
    def text(self, name):
        for p in ('defs' + BS + name.lower() + '.def', 'defs' + BS + 'interfaces' + BS + name.lower() + '.def'):
            if p in self.files:
                return _strip(open(self.files[p], 'rb').read().decode('utf-8', 'replace'))
        raise KeyError(name)

    # ---------- alias.xml ----------
    def _parse_alias(self):
        body = re.search(r'<root>(.*)</root>', self.alias_src, re.S).group(1)
        i = 0
        while True:
            m = re.compile(r'<(\w+)>').search(body, i)
            if not m:
                break
            tag = m.group(1)
            end = self._match_end(body, tag, m.end())
            self._alias[tag] = body[m.end():end].strip()
            i = end + len(tag) + 3

    @staticmethod
    def _match_end(s, tag, start):
        depth, i = 1, start
        pat = re.compile(r'<(/?)%s(\s[^>]*)?>' % re.escape(tag))
        while True:
            m = pat.search(s, i)
            if not m:
                return len(s)
            depth += -1 if m.group(1) else 1
            if depth == 0:
                return m.start()
            i = m.end()

    def resolve(self, tspec, depth=0):
        """Return a normalized type tree: ('INT32',) / ('ARRAY', sub) / ('FIXED_DICT', [(name, sub)], allowNone) ..."""
        tspec = tspec.strip()
        if depth > 30:
            raise RecursionError(tspec)
        m = re.match(r'^(ARRAY|TUPLE)\s*<of>(.*)</of>(.*)$', tspec, re.S)
        if m:
            sz = re.search(r'<size>\s*(\d+)\s*</size>', m.group(3), re.I)
            return (m.group(1), self.resolve(m.group(2), depth + 1), int(sz.group(1)) if sz else 0)
        if tspec.startswith('FIXED_DICT'):
            props = re.search(r'<Properties>(.*)</Properties>', tspec, re.S)
            fields = []
            if props:
                pb, i = props.group(1), 0
                while True:
                    mm = re.compile(r'<(\w+)>').search(pb, i)
                    if not mm:
                        break
                    tag = mm.group(1)
                    end = self._match_end(pb, tag, mm.end())
                    inner = pb[mm.end():end]
                    tt = re.search(r'<Type>(.*)</Type>', inner, re.S)
                    ts = inner.find('<Type>')
                    te = self._match_end(inner, 'Type', ts + 6) if ts >= 0 else 0
                    fd = re.search(r'<Default>(.*?)</Default>', inner[:max(ts, 0)] + inner[te:], re.S)
                    fields.append((tag, self.resolve(self._type_text(inner) if tt else 'PYTHON', depth + 1),
                                   fd.group(1).strip() if fd else None))
                    i = end + len(tag) + 3
            allow_none = bool(re.search(r'<AllowNone>\s*true\s*</AllowNone>', tspec, re.I))
            return ('FIXED_DICT', fields, allow_none)
        if tspec.startswith('USER_TYPE'):
            return ('USER_TYPE', tspec)
        word = tspec.split()[0] if tspec else 'PYTHON'
        if word in self._alias:
            return self.resolve(self._alias[word], depth + 1)
        return (word,)

    @staticmethod
    def _type_text(inner):
        """Extract <Type>...</Type> allowing nested <of>/<Properties>."""
        s = inner.find('<Type>')
        e = Defs._match_end(inner, 'Type', s + 6)
        return inner[s + 6:e]

    def section(self, t, name):
        """Body of a direct child <name> of <root>, depth-aware (inline FIXED_DICT types
        contain their own nested <Properties>, which a lazy regex would stop at)."""
        root = re.search(r'<root>', t, re.I)       # some defs use <Root> (iDroneControlAvatar)
        body = t[root.end():] if root else t
        i = 0
        while True:
            m = re.compile(r'<(\w+)(\s[^>]*)?>').search(body, i)
            if not m:
                return None
            tag = m.group(1)
            end = self._match_end(body, tag, m.end())
            if tag == name:
                return body[m.end():end]
            i = end + len(tag) + 3

    # ---------- entity properties ----------
    def properties(self, name, seen=None):
        """[(prop, typeText, flags, owner)] in parse order."""
        seen = seen if seen is not None else set()
        if name in seen:
            return []
        seen.add(name)
        t = self.text(name)
        out = []
        par = re.search(r'<Parent>\s*(\w+)\s*</Parent>', t)
        if par:
            out += self.properties(par.group(1), seen)
        impl = re.search(r'<Implements>(.*?)</Implements>', t, re.S)
        if impl:
            for itf in re.findall(r'<Interface>\s*(\w+)\s*</Interface>', impl.group(1)):
                out += self.properties(itf, seen)
        pb = self.section(t, 'Properties')
        if pb is not None:
            i = 0
            while True:
                mm = re.compile(r'<(\w+)>').search(pb, i)
                if not mm:
                    break
                tag = mm.group(1)
                end = self._match_end(pb, tag, mm.end())
                inner = pb[mm.end():end]
                if '<Type>' in inner:
                    fl = re.search(r'<Flags>\s*(\w+)\s*</Flags>', inner)
                    out.append((tag, self._type_text(inner).strip(), fl.group(1) if fl else '', name))
                    # top-level <Default> (outside the <Type> body, which may hold nested ones)
                    ts = inner.find('<Type>')
                    te = self._match_end(inner, 'Type', ts + 6) if ts >= 0 else 0
                    dm = re.search(r'<Default>(.*?)</Default>', inner[:max(ts, 0)] + inner[te:], re.S)
                    self.defaults[tag] = dm.group(1).strip() if dm else None
                i = end + len(tag) + 3
        return out

    def methods(self, name, section, seen=None):
        """[(method, [argTypeText], exposed, owner)] for 'ClientMethods'/'BaseMethods'/'CellMethods',
        in parse order (Parent, then <Implements> recursively, then own)."""
        seen = seen if seen is not None else set()
        if name in seen:
            return []
        seen.add(name)
        t = self.text(name)
        out = []
        par = re.search(r'<Parent>\s*(\w+)\s*</Parent>', t)
        if par:
            out += self.methods(par.group(1), section, seen)
        impl = re.search(r'<Implements>(.*?)</Implements>', t, re.S)
        if impl:
            for itf in re.findall(r'<Interface>\s*(\w+)\s*</Interface>', impl.group(1)):
                out += self.methods(itf, section, seen)
        body = self.section(t, section)
        if body is not None:
            i = 0
            while True:
                m = re.compile(r'<(\w+)>').search(body, i)
                if not m:
                    break
                tag = m.group(1)
                end = self._match_end(body, tag, m.end())
                inner = body[m.end():end]
                args = [a.strip() for a in re.findall(r'<Arg>(.*?)</Arg>', inner, re.S)]
                out.append((tag, args, '<Exposed/>' in inner, name))
                i = end + len(tag) + 3
        return out

    def client_method_table(self, name, dedupe='first'):
        """Client method index table. Duplicated names ('method X appears more than once')
        keep their first position."""
        out, seen = [], set()
        for m in self.methods(name, 'ClientMethods'):
            if dedupe == 'first' and m[0] in seen:
                continue
            seen.add(m[0])
            out.append(m)
        return out

    def cell_own_client_props(self, name):
        """Cell properties the owning client receives in createCellPlayer (ALL_CLIENTS, OWN_CLIENT;
        'ALL_CLIENT' is a typo variant used in some defs), same order/dedupe rule as base props."""
        order, last = [], {}
        for p in self.properties(name):
            if p[0] not in last:
                order.append(p[0])
            last[p[0]] = p
        # CELL_PUBLIC_AND_OWN is included too (confirmed: the client reads doneStartTruck /
        # gotLegionCash, both CELL_PUBLIC_AND_OWN, in parse order).
        return [last[n] for n in order if last[n][2] in ('ALL_CLIENTS', 'OWN_CLIENT', 'ALL_CLIENT', 'CELL_PUBLIC_AND_OWN')]

    def base_client_props(self, name):
        """BASE_AND_CLIENT props; a redefined name keeps its first position but takes the
        last definition (client logs 'property X is being overridden'). Athlete -> 720,
        matching the client's 'client top-level property count = 720'."""
        order, last = [], {}
        for p in self.properties(name):
            if p[0] not in last:
                order.append(p[0])
            last[p[0]] = p
        return [last[n] for n in order if last[n][2] == 'BASE_AND_CLIENT']


# ---------- serialization (BigWorld wire format) ----------
FIXED = {'INT8': '<b', 'UINT8': '<B', 'INT16': '<h', 'UINT16': '<H', 'INT32': '<i', 'UINT32': '<I',
         'INT64': '<q', 'UINT64': '<Q', 'FLOAT32': '<f', 'FLOAT64': '<d', 'FLOAT': '<f', 'BOOL': '<B'}
VECT = {'VECTOR2': 2, 'VECTOR3': 3, 'VECTOR4': 4}


def packed_len(n):
    return bytes([n]) if n < 255 else b'\xff' + struct.pack('<I', n)[:3]


def blob(b):
    return packed_len(len(b)) + b


def default_value(t):
    """Serialized zero/empty value for a resolved type tree."""
    k = t[0]
    if k in FIXED:
        return struct.pack(FIXED[k], 0)
    if k in VECT:
        return struct.pack('<%df' % VECT[k], *([0.0] * VECT[k]))
    if k in ('STRING', 'BLOB', 'UNICODE_STRING'):
        return blob(b'')
    if k in ('PYTHON', 'PY_DICT', 'PY_LIST', 'PY_TUPLE', 'PY_SIMPLE_ARRAY', 'PY_SIMPLE_TUPLE'):
        empty = {'PY_DICT': {}, 'PY_LIST': [], 'PY_TUPLE': (), 'PY_SIMPLE_ARRAY': [], 'PY_SIMPLE_TUPLE': ()}.get(k)
        return blob(pickle.dumps(empty, protocol=2))
    if k in ('ARRAY', 'TUPLE'):
        # NeoX SequenceDataType (libclient+0x9a8e5c): fixed-size sequences (<size> N) have no
        # count on the wire, just N elements; otherwise a u32 count (client read 4 bytes at
        # candidateHeros: "Invalid size on stream: 41944064" = 00 04 80 02).
        if len(t) > 2 and t[2]:
            return b''.join(default_value(t[1]) for _ in range(t[2]))
        return struct.pack('<I', 0)
    if k == 'FIXED_DICT':
        if t[2]:
            return b'\x00'          # AllowNone -> None marker
        return b''.join(encode_default(sub, fdef) for _, sub, fdef in t[1])
    raise NotImplementedError(t)


PY_LIKE = ('PYTHON', 'PY_DICT', 'PY_LIST', 'PY_TUPLE', 'PY_SIMPLE_ARRAY', 'PY_SIMPLE_TUPLE')


def encode_default(t, text):
    """Encode a property's .def <Default> text; fall back to zero/empty values.
    PYTHON without a default -> {} (client scripts call .iteritems() etc. on these;
    pickled None crashed iDtsRos2PropAthlete.onBecomePlayer)."""
    import ast
    k = t[0]
    if k == 'FIXED_DICT' and not t[2]:
        # property-level default may be nested XML: <field> value </field> ...
        nested = {}
        if text:
            for m in re.finditer(r'<(\w+)>(.*?)</\1>', text, re.S):
                nested[m.group(1)] = m.group(2).strip()
        return b''.join(encode_default(sub, nested.get(name, fdef)) for name, sub, fdef in t[1])
    if k in PY_LIKE:
        val = {}
        if text:
            try:
                val = set() if text.replace(' ', '') == 'set()' else ast.literal_eval(text)
            except Exception:
                val = {}
        elif k in ('PY_LIST', 'PY_SIMPLE_ARRAY'):
            val = []
        elif k in ('PY_TUPLE', 'PY_SIMPLE_TUPLE'):
            val = ()
        return blob(pickle.dumps(val, protocol=2))
    if text:
        try:
            if k in FIXED:
                if k.startswith('FLOAT'):
                    return struct.pack(FIXED[k], float(text))
                v = {'true': 1, 'false': 0}.get(text.lower())
                return struct.pack(FIXED[k], v if v is not None else int(float(text)))
            if k in ('STRING', 'UNICODE_STRING'):
                return blob(text.encode('utf-8'))
        except Exception:
            pass
    return default_value(t)


def stream_for(defs, entity, overrides=None, log=None, props=None):
    """Property stream with .def defaults (+ raw-bytes overrides by prop name).
    props defaults to the createBasePlayer set (BASE_AND_CLIENT)."""
    out = b''
    for prop, ttext, flags, owner in (props if props is not None else defs.base_client_props(entity)):
        t = defs.resolve(ttext)
        val = (overrides or {}).get(prop)
        enc = val if val is not None else encode_default(t, defs.defaults.get(prop))
        if log is not None:
            log.append((prop, owner, t[0], len(enc)))
        out += enc
    return out


if __name__ == '__main__':
    import sys
    D = Defs()
    ent = sys.argv[1] if len(sys.argv) > 1 else 'Athlete'
    for prop, ttext, flags, owner in D.base_client_props(ent):
        t = D.resolve(ttext)
        desc = t[0] if t[0] != 'FIXED_DICT' else 'FIXED_DICT(%d fields%s)' % (len(t[1]), ', AllowNone' if t[2] else '')
        print('%-34s %-22s %-28s %s' % (prop, owner, ' '.join(ttext.split())[:28], desc))
    log = []
    s = stream_for(D, ent, log=log)
    print('BASE_AND_CLIENT props: %d, default stream %d bytes' % (len(log), len(s)))
