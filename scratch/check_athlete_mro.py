with open(OUT, 'w') as f:
    try:
        import Athlete
        f.write('PlayerAthlete MRO: ' + repr(Athlete.PlayerAthlete.__mro__) + '\n')
        f.write('PlayerAthlete has own prerequisites? ' + repr('prerequisites' in Athlete.PlayerAthlete.__dict__) + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
