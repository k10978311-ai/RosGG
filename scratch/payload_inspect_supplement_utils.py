import sys
import traceback

with open(OUT, "w") as f:
    try:
        import supplement_utils
        f.write("supplement_utils dir:\n%r\n" % dir(supplement_utils))
        
        # Check available supplement boxes
        for attr in ["getAllSupplementIDs", "getAvailableSupplementIDs", "allSupplementDict", "allSupplements"]:
            if hasattr(supplement_utils, attr):
                val = getattr(supplement_utils, attr)
                if callable(val):
                    try:
                        val = val()
                    except Exception as e:
                        val = "error: %s" % e
                f.write("%s: %r\n" % (attr, val))
        
        # Check first 5 supplements
        if hasattr(supplement_utils, "getSupplementInfo"):
            f.write("Sample supplement infos:\n")
            for sid in [101, 102, 103, 201, 202, 301, 302, 401, 10001, 10002]:
                try:
                    info = supplement_utils.getSupplementInfo(sid)
                    if info:
                        f.write("  Box %d: %r\n" % (sid, info))
                except Exception as e:
                    pass
    except Exception:
        f.write(traceback.format_exc())
