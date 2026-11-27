# READ-ONLY: tutorial map constants and MapLoader.doLoadMap/onLoadMap names.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import const
for k in dir(const):
    if 'TUTORIAL' in k or k in ('HALL_MAP_ID',): w('const.%s=%r' % (k, getattr(const, k)))
ML = sys.modules['helpers.MapLoader'].MapLoader
for n in ('onLoadMap', 'doLoadMap', 'onHandshake'):
    co = ML.__dict__[n].func_code
    w('MapLoader.%s(%s) names=%s' % (n, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names)))
f.close()
