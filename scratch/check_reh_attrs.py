with open(OUT, 'w') as f:
    try:
        import BigWorld
        p = BigWorld.player()
        f.write('loadCompFinished: ' + repr(getattr(p, 'loadCompFinished', 'NO_ATTR')) + '\n')
        f.write('needKickOut: ' + repr(getattr(p, 'needKickOut', 'NO_ATTR')) + '\n')
        f.write('realnameAuthenAgainFlag: ' + repr(getattr(p, 'realnameAuthenAgainFlag', 'NO_ATTR')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
