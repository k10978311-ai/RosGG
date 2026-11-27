f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/acc_dict.txt', 'w')
try:
    import Account
    f.write('keys: %r\n' % sorted(Account.Account.__dict__.keys()))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
