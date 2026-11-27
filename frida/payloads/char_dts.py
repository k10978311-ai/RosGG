# READ-ONLY: characterType ids with a non-empty dts_model_path
import sys
f = open(OUT, 'w')
lp = sys.modules['player.appearance.PlayerFPAppear'].legacyProperties
rng = list(range(1, 2000)) + list(range(10000, 10300)) + list(range(20000, 20300)) + list(range(30000, 30300)) + list(range(40000, 40100)) + list(range(50000, 50100))
n = 0
for k in rng:
    try: d = lp.getCharactersData(k)
    except Exception: d = None
    if not d: continue
    n += 1
    dp = getattr(d, 'dts_model_path', None); mp = getattr(d, 'model_path', None)
    f.write('%d dts=%r model=%r gender=%r\n' % (k, dp, mp, getattr(d, 'GENDER', None)))
f.write('total %d\n' % n)
f.close()
