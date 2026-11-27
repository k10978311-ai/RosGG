with open(OUT, 'w') as f:
    try:
        import BigWorld, Athlete
        safesuper = Athlete.safesuper
        p = BigWorld.player()
        f.write('Testing safesuper enterHall with Athlete.PlayerAthlete...\n')
        safesuper(Athlete.PlayerAthlete, p).enterHall(True)
        f.write('safesuper enterHall succeeded!\n')
    except Exception as e:
        import traceback
        f.write('Error in safesuper enterHall: ' + traceback.format_exc() + '\n')
