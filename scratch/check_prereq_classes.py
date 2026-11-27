f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/prereq_classes.txt', 'w')
try:
    import Avatar, Athlete, ClientEntity
    f.write('PlayerAvatar.prerequisites is ClientEntity: %s\n' % (Avatar.PlayerAvatar.prerequisites == ClientEntity.ClientEntity.prerequisites))
    f.write('PlayerAthlete.prerequisites is ClientEntity: %s\n' % (Athlete.PlayerAthlete.prerequisites == ClientEntity.ClientEntity.prerequisites))
    f.write('Avatar.Avatar has prerequisites: %s\n' % hasattr(Avatar.Avatar, 'prerequisites'))
    f.write('Athlete.Athlete has prerequisites: %s\n' % hasattr(Athlete.Athlete, 'prerequisites'))
    import BigWorld
    f.write('BigWorld.player(): %r\n' % getattr(BigWorld, 'player', lambda: None)())
    import Globals
    f.write('Globals.player: %r\n' % getattr(Globals, 'player', 'NO_ATTR'))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
