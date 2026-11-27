f = open(OUT, 'w')
import camp_utils as cu
f.write('CampType._enum_=%r\n' % (cu.CampType._enum_,))
f.close()
