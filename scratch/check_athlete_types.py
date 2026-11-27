with open(OUT, 'w') as f:
    try:
        import BigWorld, sys
        p = BigWorld.player()
        f.write('type(p): ' + repr(type(p)) + ' id=' + str(id(type(p))) + '\n')
        import Athlete
        f.write('Athlete.PlayerAthlete: ' + repr(Athlete.PlayerAthlete) + ' id=' + str(id(Athlete.PlayerAthlete)) + '\n')
        import entities.Athlete as ath
        f.write('entities.Athlete.PlayerAthlete: ' + repr(ath.PlayerAthlete) + ' id=' + str(id(ath.PlayerAthlete)) + '\n')
        f.write('type(p) is Athlete.PlayerAthlete: ' + repr(type(p) is Athlete.PlayerAthlete) + '\n')
        f.write('type(p) is ath.PlayerAthlete: ' + repr(type(p) is ath.PlayerAthlete) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
