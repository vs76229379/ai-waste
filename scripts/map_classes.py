import os, shutil

RAW = 'data_raw/original_dataset'  # <-- change this to the folder name inside data_raw after unzip
DST = 'data_raw'  # target parent
map_biodeg = ['paper','cardboard','food','organic','leaf']
map_non = ['plastic','metal','glass','wrapper','styrofoam']

os.makedirs(os.path.join(DST,'biodegradable'), exist_ok=True)
os.makedirs(os.path.join(DST,'non_biodegradable'), exist_ok=True)

for cls in os.listdir(RAW):
    src = os.path.join(RAW,cls)
    if not os.path.isdir(src):
        continue
    if cls.lower() in map_biodeg:
        dst = os.path.join(DST,'biodegradable')
    elif cls.lower() in map_non:
        dst = os.path.join(DST,'non_biodegradable')
    else:
        dst = os.path.join(DST,'non_biodegradable')
    for f in os.listdir(src):
        if f.lower().endswith(('.jpg','.jpeg','.png')):
            shutil.copy(os.path.join(src,f), os.path.join(dst,f))
print('Mapping done')
