import os, plistlib

for root, dirs, files in os.walk("scratch"):
    for f in files:
        if f.endswith(".plist"):
            path = os.path.join(root, f)
            try:
                with open(path, "rb") as fp:
                    pl = plistlib.load(fp)
                    frames = pl.get("frames", {})
                    fb_matches = [k for k in frames.keys() if any(w in k.lower() for w in ["facebook", "fb", "pc", "login", "follow"])]
                    if fb_matches:
                        print(f"[{path}] matches:")
                        for m in fb_matches:
                            print(f"  {m} -> {frames[m].get('frame')}")
            except Exception as e:
                pass
