from PIL import Image
import os

INPUT = 'data_raw'
OUTPUT = 'data_preprocessed'
SIZE = (224,224)
os.makedirs(OUTPUT, exist_ok=True)

for cls in os.listdir(INPUT):
    src = os.path.join(INPUT, cls)
    if not os.path.isdir(src):
        continue
    dst_cls = os.path.join(OUTPUT, cls)
    os.makedirs(dst_cls, exist_ok=True)
    for f in os.listdir(src):
        if not f.lower().endswith(('.jpg','.jpeg','.png')): continue
        try:
            im = Image.open(os.path.join(src,f)).convert('RGB')
            im = im.resize(SIZE)
            im.save(os.path.join(dst_cls,f), quality=90)
        except Exception as e:
            print('skip', f, e)
print('Preprocess done')
