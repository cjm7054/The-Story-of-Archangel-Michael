import os
import requests
from PIL import Image, ImageOps

os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)

# 1. 폰트 다운로드 (나눔명조)
font_path = "assets/fonts/NanumMyeongjo.ttf"
if not os.path.exists(font_path) or os.path.getsize(font_path) < 1000:
    print("📥 나눔명조 폰트 다운로드 중...")
    r = requests.get("https://github.com/google/fonts/raw/main/ofl/nanummyeongjo/NanumMyeongjo-Regular.ttf")
    with open(font_path, "wb") as f:
        f.write(r.content)
    print("✅ 폰트 준비 완료")

# 2. 에피소드 1화 주제에 100% 일치하는 역사적 공인 가톨릭 명화 및 사진
# 위키미디어 공용(Wikimedia Commons) 퍼블릭 도메인 고해상도
scenes_images = {
    # 씬 1: 장엄한 성당 제대 (미사 제대와 십자가)
    "scene_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/High_Altar_of_the_Cathedral_of_St._John_the_Baptist%2C_Wroc%C5%82aw.jpg/1920px-High_Altar_of_the_Cathedral_of_St._John_the_Baptist%2C_Wroc%C5%82aw.jpg",
    # 씬 2: 로마 카타콤바 순교자 무덤 (지하 묘지)
    "scene_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Rome_Catacombe_Priscilla_01.jpg/1920px-Rome_Catacombe_Priscilla_01.jpg",
    # 씬 3: 초기 기독교 순교자들의 장례/추모 명화 (순교자 유해와 신자들)
    "scene_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/The_Christian_Martyr%27s_Last_Prayer%2C_by_Jean-L%C3%A9on_G%C3%A9r%C3%B4me.jpg/1920px-The_Christian_Martyr%27s_Last_Prayer%2C_by_Jean-L%C3%A9on_G%C3%A9r%C3%B4me.jpg",
    # 씬 4: 십자가의 예수 그리스도 (디에고 벨라스케스 작, 프라도 미술관)
    "scene_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Cristo_crucificado.jpg/1280px-Cristo_crucificado.jpg",
    # 씬 5: 사제의 미사 성체성사 거행 (그리스도의 몸을 들어올리는 장엄 미사)
    "scene_5.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Missa_Tridentina_-_Eleva%C3%A7%C3%A3o_do_C%C3%A1lice.jpg/1920px-Missa_Tridentina_-_Eleva%C3%A7%C3%A3o_do_C%C3%A1lice.jpg",
    # 씬 6: 성당 스테인드글라스로 쏟아지는 천상의 빛
    "scene_6.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Sainte_Chapelle_-_Upper_level.jpg/1920px-Sainte_Chapelle_-_Upper_level.jpg"
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for fname, url in scenes_images.items():
    target = os.path.join("assets/images", fname)
    print(f"📥 [{fname}] 고화질 가톨릭 성화 다운로드 중...")
    try:
        res = requests.get(url, headers=headers, timeout=25)
        if res.status_code == 200 and len(res.content) > 10000:
            with open(target, "wb") as f:
                f.write(res.content)
            # 1920x1080 리사이즈 및 크롭
            im = Image.open(target).convert("RGB")
            im = ImageOps.fit(im, (1920, 1080), Image.Resampling.LANCZOS)
            im.save(target, "JPEG", quality=95)
            print(f"✅ [{fname}] 성공 ({im.size})")
        else:
            print(f"❌ [{fname}] 다운로드 실패: 상태코드 {res.status_code}")
    except Exception as e:
        print(f"❌ [{fname}] 오류: {e}")
