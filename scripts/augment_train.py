import os, cv2
import albumentations as A
from tqdm import tqdm

# Input: preprocessed train images
INPUT = r"data_preprocessed"
OUTPUT = r"data_aug"
N_AUG = 1  # number of augmentations per original

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.08, rotate_limit=20, p=0.7),
    A.RandomBrightnessContrast(p=0.5),
    A.GaussNoise(var_limit=(5.0,30.0), p=0.3),
    A.Blur(blur_limit=3, p=0.15),
    A.Resize(224,224)
])

os.makedirs(OUTPUT, exist_ok=True)

for cls in os.listdir(INPUT):
    src_dir = os.path.join(INPUT, cls)
    if not os.path.isdir(src_dir):
        continue
    dst_dir = os.path.join(OUTPUT, cls)
    os.makedirs(dst_dir, exist_ok=True)
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    for f in tqdm(files, desc=f"Augmenting {cls}"):
        src_path = os.path.join(src_dir, f)
        img = cv2.imread(src_path)
        if img is None:
            continue
        base = os.path.splitext(f)[0]
        # save original resized copy (already 224x224 from preprocess)
        try:
            cv2.imwrite(os.path.join(dst_dir, base + '.jpg'), cv2.resize(img, (224,224)))
        except Exception:
            pass
        for i in range(N_AUG):
            aug = transform(image=img)['image']
            outname = f"{base}_aug{i}.jpg"
            cv2.imwrite(os.path.join(dst_dir, outname), aug)

print("Augmentation completed")
