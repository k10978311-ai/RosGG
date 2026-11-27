with open(OUT, 'w') as f:
    try:
        import sys
        mod = sys.modules.get('BattleGroundAvatar')
        f.write('BattleGroundAvatar mod: ' + repr(mod) + '\n')
        if mod:
            f.write('dir: ' + repr(dir(mod)) + '\n')
            cls = getattr(mod, 'BattleGroundAvatar', None) or getattr(mod, 'PlayerBattleGroundAvatar', None)
            f.write('cls: ' + repr(cls) + '\n')
            if cls:
                f.write('cls mro: ' + repr(cls.__mro__) + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
