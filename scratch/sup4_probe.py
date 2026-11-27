import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:1200] + '\n')
try:
    su = sys.modules['supplement_utils']
    fn = su.getSupplementDiscount
    c = getattr(fn, 'func_code', None)
    w('discount fn names=%r consts=%r' % (c.co_names, c.co_consts) if c else 'noc')
    for sid in (9728, 9731, 5, 1, 2):
        try: w('disc(%r) = %r' % (sid, fn(sid)))
        except Exception as e: w('disc(%r) ERR %r' % (sid, e))
    uw = [m for k, m in sys.modules.items() if k == 'ui.UIAdvanceSupplyPackage']
    w('adv mod %r' % (uw,))
except Exception:
    w(traceback.format_exc())
f.close()
