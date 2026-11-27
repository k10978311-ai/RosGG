f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/is_player.txt', 'w')
try:
    import BigWorld
    p = BigWorld.player()
    f.write('p: %r\n' % p)
    if p:
        f.write('p.isPlayer(): %r\n' % getattr(p, 'isPlayer', lambda: 'NO_ISPLAYER')())
        f.write('isinstance(p, BigWorld.Entity): %r\n' % isinstance(p, BigWorld.Entity))
        f.write('p.id: %r\n' % getattr(p, 'id', None))
        f.write('p.inWorld: %r\n' % getattr(p, 'inWorld', None))
        f.write('p.prerequisites(): %r\n' % p.prerequisites())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
