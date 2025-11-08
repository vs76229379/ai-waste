import os, shutil, random

SRC = "data_preprocessed"       # expects data_preprocessed/<class>/
DST_TRAIN = "edge_impulse_upload/train"
DST_TEST  = "edge_impulse_upload/test"
SPLIT = 0.8

# remove old upload folders if any
if os.path.exists("edge_impulse_upload"):
    shutil.rmtree("edge_impulse_upload")

os.makedirs(DST_TRAIN, exist_ok=True)
os.makedirs(DST_TEST, exist_ok=True)

total_train = 0
total_test = 0

for cls in os.listdir(SRC):
    cls_src = os.path.join(SRC, cls)
    if not os.path.isdir(cls_src):
        continue
    files = [f for f in os.listdir(cls_src) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    random.shuffle(files)
    split_idx = int(len(files) * SPLIT)
    train_files = files[:split_idx]
    test_files = files[split_idx:]

    dst_train_cls = os.path.join(DST_TRAIN, cls)
    dst_test_cls = os.path.join(DST_TEST, cls)
    os.makedirs(dst_train_cls, exist_ok=True)
    os.makedirs(dst_test_cls, exist_ok=True)

    for f in train_files:
        shutil.copy2(os.path.join(cls_src, f), os.path.join(dst_train_cls, f))
    for f in test_files:
        shutil.copy2(os.path.join(cls_src, f), os.path.join(dst_test_cls, f))

    total_train += len(train_files)
    total_test += len(test_files)
    print(f"Class {cls}: train={len(train_files)}, test={len(test_files)}")

print(f"Done. Total train={total_train}, total test={total_test}")
