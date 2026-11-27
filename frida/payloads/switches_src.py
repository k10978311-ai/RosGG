# READ-ONLY: how are URGENT_* switches populated? Dump switches-module functions referencing urgent/url/http/file.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
sw_mods = [m for m in sys.modules if m.split('.')[-1] in ('switches', 'urgent_switches', 'switch_utils') or 'urgent' in m.lower()]
w('modules: %s' % sw_mods)
def cs(co, path, depth=0):
    if depth > 3: return
    w('%s%s names=%s consts=%r' % ('  ' * depth, path, list(co.co_names)[:50], [c for c in co.co_consts if isinstance(c, (str, int)) and not isinstance(c, bool)][:25]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
for m in sw_mods:
    mod = sys.modules.get(m)
    if mod is None: continue
    w('## %s file=%s' % (m, getattr(mod, '__file__', '?')))
    for k, v in sorted(vars(mod).items()):
        if isinstance(v, types.FunctionType) and v.__module__ == m:
            cs(v.func_code, k)
    urg = sorted(k for k in vars(mod) if k.startswith('URGENT'))
    w('URGENT keys (%d): %s' % (len(urg), urg[:60]))
f.close()
