with open(OUT, 'w') as f:
    try:
        import Athlete
        for c in Athlete.PlayerAthlete.__mro__:
            if 'prerequisites' in c.__dict__:
                f.write(c.__name__ + ' defines prerequisites\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
