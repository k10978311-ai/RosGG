import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    for pid, p in lp.iterDtsHallPropData():
        if type(getattr(p, 'PROP_TYPE', None)).__name__ == 'CurrencyPropType' and pid < 60000:
            w('CUR %r %r %r' % (pid, getattr(p, 'NAME', ''), getattr(p, 'ICON_PATH', '')))
except Exception:
    w(traceback.format_exc())
f.close()
