import sys
import traceback

with open(OUT, "w") as f:
    try:
        import dts_appearance_utils
        f.write("dts_appearance_utils dir:\n%r\n" % dir(dts_appearance_utils))
        
        import tables
        f.write("tables dir:\n%r\n" % dir(tables))
        
        # Look for appearance tables
        appear_tables = [t for t in dir(tables) if any(k in t.lower() for k in ["appear", "skin", "item", "fashion", "costume"])]
        f.write("appearance tables in tables: %r\n" % appear_tables)
    except Exception:
        f.write(traceback.format_exc())
