with open(OUT, 'w') as f:
    import sys
    import Athlete
    for k, v in Athlete.__dict__.items():
        if hasattr(v, '__dict__'):
            for sk, sv in v.__dict__.items():
                if hasattr(sv, 'func_code'):
                    if 'enterHallUI' in sv.func_code.co_names:
                        f.write("found enterHallUI in %s.%s\n" % (k, sk))
