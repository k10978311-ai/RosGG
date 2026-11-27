"""Name every entry of entities.npk using the cracked NPK hash (npk_hash.py)."""
import os, re, json, struct
from npk_hash import npk_hash
BS = chr(92)
d = open('entities.npk', 'rb').read()
files, _, _, _, io = struct.unpack_from('<IIIII', d, 4)
signs = {struct.unpack_from('<I', d, io + i * 28)[0]: i for i in range(files)}
names = set()
for f in os.listdir('entities_out'):
    t = open('entities_out/' + f, 'rb').read().decode('utf-8', 'replace')
    names.update(re.findall(r'<Interface>\s*(\w+)\s*</Interface>', t))
    names.update(re.findall(r'<Parent>\s*(\w+)\s*</Parent>', t))
    names.update(re.findall(r'<ClientName>\s*(\w+)\s*</ClientName>', t))
t = re.sub(r'<!--.*?-->', '', open('entities.xml', 'rb').read().decode('utf-8', 'replace'), flags=re.S)
names.update(re.findall(r'<\s*([A-Za-z_]\w*)\s*/?>', t))
found = {}
dirs = ['defs', 'defs' + BS + 'interfaces', 'defs' + BS + 'interface', 'interfaces', 'interface', 'defs' + BS + 'components']
for n in sorted(names):
    for dd in dirs:
        p = (dd + BS + n + '.def').lower()
        h = npk_hash(p)
        if h in signs:
            found[signs[h]] = p
            break
for extra in ('entities.xml', 'alias.xml', 'defs' + BS + 'alias.xml', 'scripts' + BS + 'entity_defs' + BS + 'alias.xml'):
    h = npk_hash(extra.lower())
    if h in signs: found[signs[h]] = extra.lower()
print('named %d / %d entries' % (len(found), files))
out = {('%03d_%08x.bin' % (i, s)): found.get(i) for s, i in signs.items()}
json.dump({k: v for k, v in sorted(out.items())}, open('entities_names.json', 'w'), indent=0)
unnamed = [k for k, v in out.items() if v is None]
print('unnamed sample:', unnamed[:10])
print('dir usage:', {dd: sum(1 for v in found.values() if v.startswith(dd.lower() + BS) and v.count(BS) == dd.count(BS) + 1) for dd in dirs})
