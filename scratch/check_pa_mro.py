f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/pa_mro.txt', 'w')
try:
    import Athlete
    pa = Athlete.PlayerAthlete
    f.write('mro: %r\n' % [c.__name__ for c in pa.__mro__])
    f.write('mapID attr on class: %r\n' % getattr(pa, 'mapID', 'NOT_FOUND'))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
