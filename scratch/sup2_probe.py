import sys, traceback, time, inspect
f = open(OUT, 'w')
def w(s): f.write(s[:3000] + '\n')
try:
    su = sys.modules['supplement_utils']
    fn = su.getAvailableSupplementDictByTime
    try: w('argspec %r' % (inspect.getargspec(fn),))
    except Exception as e: w('argspec err %r' % e)
    c = getattr(fn, 'func_code', None)
    w('names %r varnames %r' % (c.co_names if c else None, c.co_varnames if c else None))
    for args in ((), (int(time.time()),), (time.time(),)):
        try:
            r = fn(*args)
            w('call%r -> type %r len %r' % (args, type(r), len(r)))
            items = list(r.items())[:6] if hasattr(r, 'items') else r
            w('sample %r' % (items,))
            break
        except Exception as e:
            w('call%r ERR %r' % (args, e))
except Exception:
    w(traceback.format_exc())
f.close()
