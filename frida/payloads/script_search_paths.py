# READ-ONLY: where does redirect.NpkImporter look for scripts (loose dir vs npk)?
# Only lookups (find_file / getattr / os.path.exists); no file writes except OUT.
import sys, os
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import redirect
C = getattr(redirect, 'C_file', None) or sys.modules.get('C_file')
w('C_file=%r' % (C,))
for k in dir(C):
    if k.startswith('__'): continue
    try: v = getattr(C, k)
    except Exception as e: v = '<err %s>' % e
    w('  C_file.%s = %r' % (k, v if not callable(v) else 'callable'))
w('importer_cache=%r' % [(k, v) for k, v in sys.path_importer_cache.items()][:20])
for imp in sys.path_importer_cache.values():
    if imp is not None and type(imp).__name__ == 'NpkImporter':
        w('NpkImporter _path=%r' % getattr(imp, '_path', None))
w('cwd=%r' % os.getcwd())
for p in ('script/ui/UILogin.nxs', 'script/ui/UILogin.py', 'ui/UILogin.nxs', 'script/redirect.nxs',
          'res/entities/loginapp.pubkey', 'entities/loginapp.pubkey'):
    try: w('find_file(%r) -> %r' % (p, C.find_file(p)))
    except Exception as e: w('find_file(%r) err %r' % (p, e))
for k in ('get_search_path', 'get_search_paths', 'get_res_path', 'get_doc_dir', 'get_root_dir', 'get_writable_dir'):
    fn = getattr(C, k, None)
    if fn:
        try: w('%s() -> %r' % (k, fn()))
        except Exception as e: w('%s() err %r' % (k, e))
try:
    import game3d
    for k in dir(game3d):
        if any(s in k.lower() for s in ('path', 'dir', 'root', 'doc')):
            v = getattr(game3d, k)
            try: w('game3d.%s() -> %r' % (k, v() if callable(v) else v))
            except Exception as e: w('game3d.%s err %r' % (k, e))
except Exception as e:
    w('game3d err %r' % e)
f.close()
