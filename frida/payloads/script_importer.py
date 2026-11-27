# READ-ONLY: describe the NeoX script importer (how script.npk entries are decrypted).
# Dumps meta_path/path_hooks objects, their methods' consts/names, and marshals their code
# objects to files/importer_code.bin for offline disassembly. Calls no game logic.
import sys, types, marshal
f = open(OUT, 'w')
def w(s): f.write(s + '\n')

codes = {}
def desc_code(co, path, depth=0):
    if depth > 4: return
    codes[path] = co
    w('  CODE %s file=%s names=%r' % (path, co.co_filename, list(co.co_names)))
    w('       consts=%r' % ([c for c in co.co_consts if not isinstance(c, types.CodeType)],))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): desc_code(c, path + '.' + c.co_name, depth + 1)

def desc_obj(o, label):
    t = type(o)
    w('%s: %r type=%s module=%s' % (label, o, t.__name__, getattr(t, '__module__', '?')))
    for k in dir(o):
        if k.startswith('__') and k not in ('__init__', '__call__'): continue
        try: v = getattr(o, k)
        except Exception as e: w('  attr %s <err %s>' % (k, e)); continue
        fn = getattr(v, 'im_func', v)
        co = getattr(fn, 'func_code', None)
        if co is not None: desc_code(co, '%s.%s' % (t.__name__, k))
        elif not callable(v): w('  attr %s = %r' % (k, v if not isinstance(v, str) else v[:200]))
    try:
        mod = sys.modules.get(t.__module__)
        if mod is not None:
            w('  module %s file=%s' % (t.__module__, getattr(mod, '__file__', None)))
            for k, v in sorted(vars(mod).items()):
                if isinstance(v, (str, int, long)) and not k.startswith('__'):
                    w('  modvar %s = %r' % (k, v if not isinstance(v, str) else v[:300]))
                elif isinstance(v, types.FunctionType):
                    desc_code(v.func_code, '%s:%s' % (t.__module__, k))
    except Exception as e:
        w('  module err %r' % e)

w('meta_path=%r' % (sys.meta_path,))
w('path_hooks=%r' % (sys.path_hooks,))
w('path=%r' % (sys.path[:10],))
for i, o in enumerate(sys.meta_path): desc_obj(o, 'meta_path[%d]' % i)
for i, o in enumerate(sys.path_hooks): desc_obj(o, 'path_hooks[%d]' % i)
w('rotor in modules: %r' % ('rotor' in sys.modules,))
for name in ('redirect', 'nxs', '_redirect', 'npk_importer'):
    if name in sys.modules: desc_obj(sys.modules[name], 'module ' + name)
w('modules with rotor/npk/redirect: %r' % [m for m in sys.modules if any(s in m.lower() for s in ('rotor', 'npk', 'redirect', 'nxs', 'import'))])
try:
    open(OUT.replace('py_out.log', 'importer_code.bin'), 'wb').write(marshal.dumps(dict((k, v) for k, v in codes.items())))
    w('marshalled %d code objects' % len(codes))
except Exception as e:
    w('marshal err %r' % e)
f.close()
