with open(OUT, 'w') as f:
    try:
        import BigWorld, Globals
        p = BigWorld.player()
        f.write('BigWorld.player: ' + repr(p) + '\n')
        f.write('type: ' + str(type(p)) + '\n')
        f.write('MAP_ID: ' + str(getattr(Globals, 'MAP_ID', 'None')) + '\n')
        f.write('enterFirstFlag: ' + str(getattr(Globals, 'enterFirstFlag', 'None')) + '\n')
        f.write('rookieEnterHall: ' + str(getattr(Globals, 'rookieEnterHall', 'None')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
