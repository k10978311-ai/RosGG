f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/pa_hall_m.txt', 'w')
try:
    import Athlete
    for m in dir(Athlete.PlayerAthlete):
        if 'hall' in m.lower():
            f.write('%s\n' % m)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
