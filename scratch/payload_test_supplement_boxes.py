import supplement_utils as su
import traceback

with open(OUT, "w") as f:
    try:
        avail = su.getAvailableSupplementDictByTime()
        f.write("Available supplements by time: %d\n" % len(avail))
        for box_id in sorted(avail.keys())[:15]:
            name = su.getSupplementName(box_id)
            kind = su.getSupplementKindName(box_id)
            props = su.getAllPossiblePropID(box_id)
            f.write("\nBox %d: Name=%r, Kind=%r, PossiblePropsCount=%d\n" % (box_id, name, kind, len(props)))
            if props:
                f.write("  Sample props: %r\n" % props[:10])
    except Exception:
        f.write(traceback.format_exc())
