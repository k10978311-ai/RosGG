import sys, dts_const
out = open(OUT, 'w')
out.write('DEFAULT_COLD_WEAPON: %s\n' % getattr(dts_const, 'DEFAULT_COLD_WEAPON', None))
out.write('DEFAULT_COLD_WEAPON_IDS: %s\n' % getattr(dts_const, 'DEFAULT_COLD_WEAPON_IDS', None))
out.write('HAND_WEAPON_SLOT: %s\n' % getattr(dts_const, 'HAND_WEAPON_SLOT', None))
out.write('COLD_WEAPON_SLOT: %s\n' % getattr(dts_const, 'COLD_WEAPON_SLOT', None))
out.close()
