with open(OUT, 'w') as f:
    try:
        import BigWorld
        p = BigWorld.player()
        f.write('loadCompFinished: ' + repr(getattr(p, 'loadCompFinished', 'NOT_SET')) + '\n')
        f.write('realnameAuthenAgainFlag: ' + repr(getattr(p, 'realnameAuthenAgainFlag', 'NOT_SET')) + '\n')
        f.write('needKickOut: ' + repr(getattr(p, 'needKickOut', 'NOT_SET')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
