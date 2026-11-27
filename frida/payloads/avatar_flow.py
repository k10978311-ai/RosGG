# READ-ONLY: PlayerAvatar map-load flow. Dumps (unwrapped) bodies of key methods and finds
# who calls loadMap / where currentMapID comes from.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import Avatar
def unwrap(fn):
    for cell in (getattr(fn, 'func_closure', None) or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): return unwrap(v)
    return fn
def dump(cls, name):
    for c in cls.__mro__:
        fn = c.__dict__.get(name)
        if isinstance(fn, types.FunctionType):
            g = unwrap(fn); co = g.func_code
            w('%s.%s(%s) names=%s consts=%r' % (c.__name__, name, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names)[:60], [x for x in co.co_consts if isinstance(x, (str, int))][:20]))
            return
    w('%s.%s: not found' % (cls.__name__, name))
PA = Avatar.PlayerAvatar
w('MRO len=%d first=%s' % (len(PA.__mro__), [c.__name__ for c in PA.__mro__][:8]))
for n in ('onBecomePlayer', 'enterWorld', 'onEnterWorld', 'loadMap', 'initLevel', 'set_currentMapID', 'onEnterSpace', 'prerequisites'):
    dump(PA, n)
# who references currentMapID / loadMap (unwrapped)
seen = set()
def walk(co, path, d=0):
    if d > 6 or id(co) in seen: return
    seen.add(id(co))
    if ('loadMap' in co.co_names or 'currentMapID' in co.co_names) and 'Avatar' in path:
        w('REF %s names=%s' % (path, list(co.co_names)[:30]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk(c, path + '.' + c.co_name, d + 1)
for c in PA.__mro__:
    for k, v in c.__dict__.items():
        if isinstance(v, types.FunctionType):
            walk(unwrap(v).func_code, '%s.%s' % (c.__name__, k))
f.close()
