with open(OUT, 'w') as f:
    try:
        import entities.Athlete as ath
        import types
        hits = []
        for k, v in ath.PlayerAthlete.__dict__.items():
            fn = getattr(v, 'im_func', v)
            if hasattr(fn, 'func_code'):
                co = fn.func_code
                if 'loadCompFinished' in co.co_names:
                    hits.append(k)
        f.write('Methods referencing loadCompFinished: ' + repr(hits) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
