with open(OUT, 'w') as f:
    try:
        import sys
        mod = sys.modules.get('BattleGroundAvatar')
        cls = getattr(mod, 'PlayerBattleGroundAvatar', None)
        f.write('PlayerBattleGroundAvatar: ' + repr(cls) + '\n')
        f.write('MRO: ' + repr(cls.__mro__) + '\n')
        f.write('dir: ' + repr(dir(cls)) + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
