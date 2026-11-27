with open(OUT, 'w') as f:
    import Athlete
    cls = Athlete.PlayerAthlete
    f.write("cls.mapID: %r\n" % getattr(cls, 'mapID', 'NOT_FOUND'))
    import Globals
    f.write("Globals.MAP_ID: %r\n" % getattr(Globals, 'MAP_ID', None))
    f.write("Globals.player: %r\n" % getattr(Globals, 'player', None))
