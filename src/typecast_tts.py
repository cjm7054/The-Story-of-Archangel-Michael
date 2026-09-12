import os
import time
import requests
import json

class TypecastTTS:
    """
    Typecast API를 활용한 음성 생성 클라이언트
    """
    BASE_URL = "https://typecast.ai/api"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TYPECAST_API_KEY")
        if not self.api_key:
            raise ValueError("TYPECAST_API_KEY가 설정되지 않았습니다.")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def synthesize(self, text: str, output_path: str, actor_id: str = "tc_61c0282465e94b8e88e14674", tempo: float = 0.95):
        """
        주어진 텍스트를 음성(wav/mp3)으로 생성하여 파일로 저장합니다.
        필재 배우 또는 지정된 actor_id를 사용합니다.
        """
        payload = {
            "text": text,
            "lang": "ko",
            "actor_id": actor_id,
            "tempo": tempo,
            "volume": 100,
            "pitch": 0,
            "xapi_hd": True,
            "model_version": "latest"
        }

        print(f"🎙️ [Typecast TTS] 요청 중: {text[:30]}...")
        # 1. 합성 요청 (Speak API)
        response = requests.post(f"{self.BASE_URL}/speak", headers=self.headers, json=payload)
        
        if response.status_code != 200:
            # v1 엔드포인트 대체 시도
            fallback_res = requests.post("https://api.typecast.ai/v1/speak", headers=self.headers, json=payload)
            if fallback_res.status_code != 200:
                raise RuntimeError(f"Typecast API 에러 ({response.status_code}): {response.text}")
            response = fallback_res

        data = response.json()
        
        # Polling 결과 확인 (대부분 speak_url 반환)
        result = data.get("result", {})
        audio_url = result.get("speak_v2_url") or result.get("audio_download_url") or data.get("audio_url")
        
        # 진행 중일 경우 polling
        if not audio_url and "speak_url" in result:
            poll_url = result["speak_url"]
            print("⏳ 음성 생성 대기 중...")
            for _ in range(30):
                time.sleep(1.5)
                poll_res = requests.get(poll_url, headers=self.headers)
                if poll_res.status_code == 200:
                    p_data = poll_res.json()
                    p_result = p_data.get("result", {})
                    status = p_result.get("status")
                    if status == "done":
                        audio_url = p_result.get("speak_v2_url") or p_result.get("audio_download_url")
                        break
                    elif status == "failed":
                        raise RuntimeError(f"TTS 생성 실패: {p_data}")

        if not audio_url:
            raise RuntimeError(f"오디오 다운로드 URL을 받지 못했습니다: {data}")

        # 2. 오디오 파일 다운로드
        audio_res = requests.get(audio_url)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(audio_res.content)
        
        print(f"✅ 오디오 저장 완료: {output_path}")
        return output_path
