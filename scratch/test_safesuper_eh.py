with open(OUT, 'w') as f:
    try:
        import BigWorld, entities.Athlete as ath
        safesuper = ath.safesuper
        p = BigWorld.player()
        f.write('Testing safesuper enterHall...\n')
        safesuper(ath.PlayerAthlete, p).enterHall(True)
        f.write('safesuper enterHall succeeded!\n')
    except Exception as e:
        import traceback
        f.write('Error in safesuper enterHall: ' + traceback.format_exc() + '\n')
