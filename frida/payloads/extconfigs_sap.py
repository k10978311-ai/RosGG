# READ-ONLY: what does extconfigs.getServiceAccessPoint look up?
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import extconfigs
fn = extconfigs.getServiceAccessPoint
co = fn.func_code
w('args=%s names=%s consts=%r' % (co.co_varnames[:co.co_argcount], list(co.co_names), [c for c in co.co_consts if not isinstance(c, types.CodeType)]))
for name in co.co_names:
    v = getattr(extconfigs, name, None)
    if isinstance(v, dict):
        w('extconfigs.%s keys=%r' % (name, list(v.keys())[:30]))
f.close()
