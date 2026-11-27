import glob, re

for p in glob.glob('decompile/apk_unzip/res/**/strings*.xml', recursive=True):
    with open(p, 'rb') as f:
        data = f.read()
    if b'Invalid login. Please log in again' in data:
        print('Found in', p)
        for m in re.finditer(rb'<string name="([^"]+)"[^>]*>([^<]*Invalid login[^<]*)</string>', data):
            print(' ', m.group(1).decode(), '->', m.group(2).decode())
