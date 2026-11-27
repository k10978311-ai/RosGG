with open(OUT, 'w') as f:
    try:
        import sys, types, dis
        # Look for code that has 'player' and 'set' or assigns to player
        for modname, mod in sys.modules.items():
            if not mod or not modname.startswith(('Player', 'entities', 'Athlete', 'Avatar', 'ClientEntity', 'Globals', 'GameInit')):
                continue
            for k, v in mod.__dict__.items():
                objs = [v]
                if isinstance(v, (type, types.ClassType)):
                    objs += [getattr(v, m) for m in dir(v)]
                for obj in objs:
                    fn = getattr(obj, 'im_func', obj)
                    co = getattr(fn, 'func_code', None)
                    if not co: continue
                    if 'player' in co.co_names:
                        # disassemble and check
                        import StringIO
                        buf = StringIO.StringIO()
                        old = sys.stdout; sys.stdout = buf
                        dis.dis(fn)
                        sys.stdout = old
                        dis_txt = buf.getvalue()
                        # check if STORE_ATTR or STORE_GLOBAL with player
                        for line in dis_txt.splitlines():
                            if 'player' in line and any(w in line for w in ('STORE', 'ATTR', 'GLOBAL', '<156>')):
                                f.write('%s in %s: %s\n' % (k, modname, line))
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
