f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import PlayerAthlete
    cls = PlayerAthlete.PlayerAthlete
    f.write('PlayerAthlete mro: %r\n' % [c.__name__ for c in cls.__mro__])
    for c in cls.__mro__:
        if 'prerequisites' in c.__dict__:
            f.write('prerequisites defined in: %s\n' % c.__name__)
        if 'enterWorld' in c.__dict__:
            f.write('enterWorld defined in: %s\n' % c.__name__)
        if 'onBecomePlayer' in c.__dict__:
            f.write('onBecomePlayer defined in: %s\n' % c.__name__)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
