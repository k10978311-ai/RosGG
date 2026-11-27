with open(OUT, 'w') as f:
    try:
        import entities.Athlete as ath
        f.write('MRO: ' + repr([c.__name__ for c in ath.PlayerAthlete.__mro__]) + '\n')
        for c in ath.PlayerAthlete.__mro__:
            if 'enterHall' in c.__dict__:
                f.write('enterHall defined in: ' + c.__name__ + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
