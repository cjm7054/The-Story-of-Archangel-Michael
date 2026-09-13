import os
import requests

ASSETS_DIR = "assets"
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)

# 1. Download official Nanum font (NanumMyeongjo / NanumGothic)
font_url = "https://github.com/google/fonts/raw/main/ofl/nanummyeongjo/NanumMyeongjo-Regular.ttf"
font_path = os.path.join(FONTS_DIR, "NanumMyeongjo.ttf")
print("Downloading NanumMyeongjo font...")
res = requests.get(font_url)
with open(font_path, "wb") as f:
    f.write(res.content)
print(f"Font saved: {font_path} ({os.path.getsize(font_path)} bytes)")

# 2. Curated High Quality Public Domain Catholic Paintings/Photos from Wikimedia
images = {
    # 씬 1: 촛불 켜진 성당 제대 (Altar with candles)
    "scene_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/High_Altar_of_the_Cathedral_of_St._John_the_Baptist%2C_Wroc%C5%82aw.jpg/1920px-High_Altar_of_the_Cathedral_of_St._John_the_Baptist%2C_Wroc%C5%82aw.jpg",
    # 씬 2: 로마 카타콤바 순교자 석관/벽화 (Catacombs of Priscilla / Callixtus)
    "scene_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Rome_Catacombe_Priscilla_01.jpg/1920px-Rome_Catacombe_Priscilla_01.jpg",
    # 씬 3: 초기 기독교 순교자 명화 (Christian martyrs painting)
    "scene_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Siemiradzki_Dirce.jpg/1920px-Siemiradzki_Dirce.jpg",
    # 씬 4: 십자가의 예수 그리스도 명화 (Crucifixion by Velazquez)
    "scene_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Cristo_crucificado.jpg/1280px-Cristo_crucificado.jpg",
    # 씬 5: 성체성사 거행하는 사제 명화 (The Last Supper / Mass)
    "scene_5.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/%C3%9Altima_Cena_-_Da_Vinci_5.jpg/1920px-%C3%9Altima_Cena_-_Da_Vinci_5.jpg",
    # 씬 6: 성당 스테인드글라스 빛 (Stained glass light)
    "scene_6.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Sainte_Chapelle_-_Upper_level.jpg/1920px-Sainte_Chapelle_-_Upper_level.jpg"
}

headers = {"User-Agent": "CatholicVideoMaker/1.0 (contact: catholic@example.com)"}

for filename, url in images.items():
    target = os.path.join(IMAGES_DIR, filename)
    print(f"Downloading {filename}...")
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            with open(target, "wb") as f:
                f.write(r.content)
            print(f"Saved {target} ({os.path.getsize(target)} bytes)")
        else:
            print(f"Failed {filename}: status {r.status_code}")
    except Exception as e:
        print(f"Error {filename}: {e}")
