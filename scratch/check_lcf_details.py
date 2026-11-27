with open(OUT, 'w') as f:
    try:
        import BigWorld, entities.Athlete as ath
        p = BigWorld.player()
        f.write('p.loadCompFinished: ' + repr(p.loadCompFinished) + '\n')
        f.write('p.__dict__ has loadCompFinished: ' + repr('loadCompFinished' in p.__dict__) + '\n')
        f.write('Athlete.PlayerAthlete.loadCompFinished: ' + repr(getattr(ath.PlayerAthlete, 'loadCompFinished', 'NOT_ON_CLASS')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
