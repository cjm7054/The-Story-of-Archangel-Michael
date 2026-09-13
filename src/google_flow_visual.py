import os
import io
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class GoogleFlowVisual:
    """
    Google Flow / Imagen 3 AI 이미지 생성 엔진
    각 씬별 가톨릭 주제에 맞추어 16:9 비율의 초고화질 시네마틱 이미지를 직접 생성합니다.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("🌟 [Google Flow / Imagen] 구글 AI 클라이언트 초기화 완료")
            except Exception as e:
                print(f"⚠️ [Google Flow] 초기화 경고: {e}")

    def generate_image(self, prompt: str, output_path: str, fallback_url: str = None):
        """
        Imagen 3를 통해 시네마틱 성화/배경 생성 (실패 시 고화질 공인 명화 URL로 안전 대체)
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if self.client:
            try:
                # 신비한 건축사전 및 내셔널지오그래픽 다큐멘터리 스타일 프롬프트 보강
                refined_prompt = (
                    f"Cinematic documentary shot, high production value, photorealistic, 8k resolution, "
                    f"dramatic volumetric lighting, solemn Catholic atmosphere: {prompt}"
                )
                print(f"🎨 [Google Imagen 3] 고화질 이미지 생성 요청 중: {prompt[:35]}...")
                
                result = self.client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=refined_prompt,
                    config=dict(
                        number_of_images=1,
                        aspect_ratio="16:9",
                        person_generation="ALLOW_ADULT",
                        output_mime_type="image/jpeg"
                    )
                )

                for generated_image in result.generated_images:
                    image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                    image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
                    image.save(output_path, "JPEG", quality=95)
                    print(f"✅ [Google Imagen 3] 1080p 시네마틱 이미지 생성 완료: {output_path}")
                    return output_path
            except Exception as e:
                print(f"⚠️ [Google Imagen 3] 생성 오류: {e}")

        # Gemini/Imagen 키가 없거나 생성 실패 시, 사전에 검증된 공인 고화질 성화 URL로 안전 다운로드
        if fallback_url:
            print(f"📥 [Fallback] 공인 고화질 성화 에셋 로드 중: {fallback_url}")
            import requests
            from PIL import ImageOps
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(fallback_url, headers=headers, timeout=20)
            if r.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(r.content)
                im = Image.open(output_path).convert("RGB")
                im = ImageOps.fit(im, (1920, 1080), Image.Resampling.LANCZOS)
                im.save(output_path, "JPEG", quality=95)
                return output_path

        # 기본 배경 생성
        fallback_img = Image.new("RGB", (1920, 1080), color=(15, 23, 42))
        fallback_img.save(output_path, "JPEG", quality=95)
        return output_path
