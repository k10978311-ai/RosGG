import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("player: %r\n" % p)
        
        # Test adding one item
        item_id = 120901
        item_data = {
            "uuid": "testuuid12345678",
            "itemID": item_id,
            "number": 1,
            "info": {}
        }
        
        # Check current items before
        f.write("items before: %r\n" % getattr(p.dtsAppearancePackage, "itemList", None))
        
        # Call onAddDtsAppearanceItem
        # args: (itemID, changedItemList, itemSrc, number, remainSec, day)
        p.onAddDtsAppearanceItem(item_id, [item_data], 0, 1, 0, 0)
        
        # Check items after
        items_after = getattr(p.dtsAppearancePackage, "itemList", None)
        f.write("items after: %r\n" % items_after)
        f.write("has item 120901: %r\n" % p.getDtsAppearanceCnt(item_id))
    except Exception:
        f.write(traceback.format_exc())
