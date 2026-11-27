f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import Athlete
    cls = Athlete.PlayerAthlete
    f.write('MRO: %r\n' % [c.__name__ for c in cls.__mro__])
    for c in cls.__mro__:
        for m in ['prerequisites', 'enterWorld', 'onBecomePlayer', 'enterHall', '_realEnterHall', 'onLogin', 'showSelectCharacter']:
            if m in c.__dict__:
                f.write('%s has %s\n' % (c.__name__, m))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
