f = open(OUT, "w")
try:
    import BattleGroundAvatar, Avatar, PlayerAvatar, ClientEntity
    for cls in (BattleGroundAvatar.BattleGroundAvatar, Avatar.Avatar, PlayerAvatar.PlayerAvatar, ClientEntity.ClientEntity):
        if 'prerequisites' in cls.__dict__:
            f.write("prerequisites in %s\n" % cls.__name__)
        else:
            f.write("no prerequisites in %s\n" % cls.__name__)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
