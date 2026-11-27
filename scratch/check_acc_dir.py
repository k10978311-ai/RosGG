f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/acc_dir.txt', 'w')
try:
    import Account
    f.write('dir: %r\n' % [k for k in dir(Account.Account) if 'login' in k.lower() or 'scene' in k.lower() or 'channel' in k.lower()])
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
