f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/acc_mro.txt', 'w')
try:
    import Account
    f.write('Account mro: %r\n' % [c.__name__ for c in Account.Account.__mro__])
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
