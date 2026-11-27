import package_common.PackageConvert3 as pconv
import traceback

with open(OUT, "w") as f:
    try:
        c = pconv.dtsAppearancePackageConvert3
        f.write("converter: %r\n" % c)
        
        # Test converting dictionary with ITEM_DATA3 records
        sample_item_data = {
            "uuid": "\x01" * 16,
            "itemID": 120901,
            "number": 1,
            "info": {}
        }
        
        # In BigWorld FIXED_DICT deserialization, what dictionary does it pass to createObjFromDict?
        d = {
            "itemList": [sample_item_data],
            "itemsList": [],
            "layoutInfo": {},
            "_packageCapacity": 200
        }
        obj = c.createObjFromDict(d)
        f.write("created obj: %r\n" % obj)
        f.write("created obj itemList: %r\n" % getattr(obj, "itemList", None))
        
        # What if itemsList has it?
        d_items = {
            "itemList": [],
            "itemsList": [[sample_item_data]],
            "layoutInfo": {},
            "_packageCapacity": 200
        }
        obj2 = c.createObjFromDict(d_items)
        f.write("created obj2 itemList: %r\n" % getattr(obj2, "itemList", None))

    except Exception:
        f.write(traceback.format_exc())
