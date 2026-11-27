with open(OUT, 'w') as f:
    import BigWorld, Globals, sys
    f.write("player: %r\n" % (getattr(BigWorld, 'player', lambda: None)()))
    f.write("entities: %r\n" % (list(BigWorld.entities.keys()) if hasattr(BigWorld, 'entities') else None))
    f.write("Globals.MAP_ID: %r\n" % (getattr(Globals, 'MAP_ID', None)))
    f.write("Globals.inLoading: %r\n" % (getattr(Globals, 'inLoading', None)))
    f.write("Globals.inLoadingStage1: %r\n" % (getattr(Globals, 'inLoadingStage1', None)))
    p = BigWorld.player()
    if p:
        f.write("p.id: %r, p.spaceID: %r\n" % (getattr(p, 'id', None), getattr(p, 'spaceID', None)))
        f.write("p.mapID: %r\n" % (getattr(p, 'mapID', None)))
        f.write("p.base: %r\n" % (getattr(p, 'base', None)))
    import UIMgr
    f.write("UIMgr.ui_list: %r\n" % ([ui.__class__.__name__ for ui in getattr(UIMgr, '_ui_list', [])]))
