with open(OUT, 'w') as f:
    import Avatar
    pa = Avatar.PlayerAvatar
    for m in dir(pa):
        if any(w in m.lower() for w in ['space', 'leave', 'transfer', 'exit', 'hall', 'finish']):
            f.write("pa.%s: %r\n" % (m, getattr(pa, m)))
