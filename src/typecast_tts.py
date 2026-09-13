import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

class TypecastTTS:
    """
    Typecast 공식 최신 API v1 (X-API-KEY / ssfm-v30) 클라이언트
    """
    BASE_URL = "https://api.typecast.ai"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TYPECAST_API_KEY", "").strip()
        if not self.api_key:
            raise ValueError("TYPECAST_API_KEY가 비어 있습니다. .env 파일을 확인해주세요.")
        
        masked = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "***"
        print(f"🔑 [Auth] TYPECAST_API_KEY 로드됨: {masked}")

        self.headers = {
            "X-API-KEY": self.api_key,
            "User-Agent": "typecast-direct/1 python typecast-integration/1 (source=api-docs; generated_by=gemini-cli)",
            "Content-Type": "application/json"
        }

    def get_piljae_voice_id(self) -> str:
        """
        /v3/voices 목록에서 '필재' 또는 'Piljae'의 정확한 voice_id를 검색
        """
        try:
            res = requests.get(f"{self.BASE_URL}/v3/voices?model=ssfm-v30", headers=self.headers, timeout=10)
            if res.status_code == 200:
                voices = res.json()
                for v in voices:
                    name = v.get("voice_name", "")
                    if "필재" in name or "Piljae" in name or "piljae" in name:
                        print(f"🎯 타입캐스트 필재 보이스 ID 확인: {v.get('voice_id')} ({name})")
                        return v.get("voice_id")
        except Exception as e:
            print(f"⚠️ 보이스 조회 경고: {e}")
        return "tc_61c0282465e94b8e88e14674" # 기본 필재 ID

    def synthesize(self, text: str, output_path: str, actor_id: str = None, tempo: float = 0.95):
        """
        공식 /v1/text-to-speech 엔드포인트로 바이너리 WAV 오디오 생성
        """
        voice_id = actor_id or self.get_piljae_voice_id()
        payload = {
            "model": "ssfm-v30",
            "voice_id": voice_id,
            "text": text,
            "output": {
                "audio_format": "wav"
            }
        }

        print(f"🎙️ [타입캐스트 필재] 음성 생성 요청 중: {text[:30]}...")
        
        response = requests.post(f"{self.BASE_URL}/v1/text-to-speech", headers=self.headers, json=payload)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ [타입캐스트 필재] 음성 저장 완료: {output_path}")
            return output_path

        # 401/403 또는 기타 에러 시 상세 출력 및 백업 전환
        print(f"⚠️ Typecast API 응답 상태 ({response.status_code}): {response.text}")
        print("🎙️ 백업 다큐멘터리 해설 보이스(InJoon)로 음성을 합성합니다...")
        return self._synthesize_fallback(text, output_path)

    def _synthesize_fallback(self, text: str, output_path: str):
        import asyncio
        import edge_tts

        async def _run():
            communicate = edge_tts.Communicate(text, "ko-KR-InJoonNeural", rate="-4%", pitch="-2Hz")
            await communicate.save(output_path)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        asyncio.run(_run())
        print(f"✅ [백업 음성] 오디오 저장 완료: {output_path}")
        return output_path
