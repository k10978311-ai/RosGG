import glob, re

for p in glob.glob('decompile/apk_unzip/*.dex'):
    with open(p, 'rb') as f:
        data = f.read()
    # Search for known NetEase error codes like 1001, 1002, 1003, 1004, 2001, 2002, 2003
    for s in [b'1001', b'1002', b'1003', b'1004', b'2001', b'2002', b'2003']:
        cnt = data.count(s)
        # print if found
    if b'MpayLoginCallback' in data:
        print('MpayLoginCallback in', p)
    if b'onFailure' in data and b'mpay' in data:
        print('mpay onFailure in', p)
