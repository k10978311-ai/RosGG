with open(OUT, 'w') as f:
    try:
        import entities.Athlete as ath
        hits = []
        for cls in ath.PlayerAthlete.__mro__:
            for k, v in cls.__dict__.items():
                fn = getattr(v, 'im_func', v)
                if hasattr(fn, 'func_code'):
                    co = fn.func_code
                    if 'loadCompFinished' in co.co_names:
                        hits.append((cls.__name__, k))
        f.write('MRO hits: ' + repr(hits) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
