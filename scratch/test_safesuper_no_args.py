with open(OUT, 'w') as f:
    try:
        import BigWorld, Athlete
        p = BigWorld.player()
        f.write('Calling safesuper(Athlete.PlayerAthlete, p).enterHall()...\n')
        Athlete.safesuper(Athlete.PlayerAthlete, p).enterHall()
        f.write('SUCCESS! safesuper enterHall returned cleanly!\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
