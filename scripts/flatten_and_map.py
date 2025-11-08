import os, shutil

BASE = "data_raw"
DST_BIO = os.path.join(BASE, "biodegradable")
DST_NON = os.path.join(BASE, "non_biodegradable")
os.makedirs(DST_BIO, exist_ok=True)
os.makedirs(DST_NON, exist_ok=True)

# keywords to decide mapping (case-insensitive substring match)
bio_keys = ["paper","cardboard","food","organic","leaf","banana","peel","vegetable","fruit","newspaper"]
non_keys = ["plastic","metal","glass","wrapper","styrofoam","can","bottle","bag","poly","plastic_bottle","plasticwrap"]

copied = 0
skipped = 0

# walk recursively and copy image files
for root, dirs, files in os.walk(BASE):
    # skip the target folders themselves to avoid copying already-copied files
    if os.path.abspath(root) in (os.path.abspath(DST_BIO), os.path.abspath(DST_NON)):
        continue
    for f in files:
        if not f.lower().endswith(('.jpg','.jpeg','.png')):
            continue
        src_path = os.path.join(root, f)
        # decide destination by checking all parts of path + filename
        path_lower = (root + os.sep + f).lower()
        dest = DST_NON  # default
        if any(k in path_lower for k in bio_keys):
            dest = DST_BIO
        elif any(k in path_lower for k in non_keys):
            dest = DST_NON
        else:
            dest = DST_NON
        # avoid overwriting: if same name exists, add suffix
        out_path = os.path.join(dest, f)
        if os.path.exists(out_path):
            base, ext = os.path.splitext(f)
            i = 1
            while os.path.exists(os.path.join(dest, f"{base}_dup{i}{ext}")):
                i += 1
            out_path = os.path.join(dest, f"{base}_dup{i}{ext}")
        try:
            shutil.copy2(src_path, out_path)
            copied += 1
        except Exception as e:
            print("skip", src_path, e)
            skipped += 1

print(f"Done. Copied: {copied}, Skipped: {skipped}")
