with open(OUT, 'w') as f:
    try:
        import sys
        f.write('Avatar modules: ' + repr([k for k in sys.modules if 'Avatar' in k or 'Athlete' in k or 'Account' in k]) + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
