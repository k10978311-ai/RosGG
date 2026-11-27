import sys, traceback
out = open(OUT, 'w')
try:
    import sys
    uis = []
    for m in sys.modules.values():
        if m and hasattr(m, '__dict__'):
            for k in m.__dict__.keys():
                if 'SelectCharacter' in k or 'createCharacter' in k or 'CreateRole' in k:
                    uis.append((m.__name__, k))
    out.write('Found classes/functions:\n')
    for mod, k in uis:
        out.write('  %s.%s\n' % (mod, k))
except Exception:
    out.write(traceback.format_exc())
out.close()
