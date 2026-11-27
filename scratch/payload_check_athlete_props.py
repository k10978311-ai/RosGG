import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("player: %r\n" % p)
        for attr in ["playerName", "baseNickname", "freeYuanbao", "payYuanbao", "baseLevel", "currencyList", "currencies"]:
            if hasattr(p, attr):
                f.write("%s: %r\n" % (attr, getattr(p, attr)))
    except Exception:
        f.write(traceback.format_exc())
