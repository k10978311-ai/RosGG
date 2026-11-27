with open(OUT, 'w') as f:
    import BigWorld, Globals, sys
    f.write("Globals.player: %r\n" % getattr(Globals, 'player', None))
    # Search modules for Athlete
    for mod_name, mod in sys.modules.items():
        if hasattr(mod, 'PlayerAthlete') or hasattr(mod, 'Athlete'):
            f.write("found in %s: %r\n" % (mod_name, getattr(mod, 'PlayerAthlete', getattr(mod, 'Athlete', None))))
    import game_entities
    f.write("game_entities: %r\n" % dir(game_entities))
