import os
import time
import requests
import json

class TypecastTTS:
    """
    Typecast API를 활용한 음성 생성 클라이언트
    """
    BASE_URL = "https://api.typecast.ai"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TYPECAST_API_KEY", "").strip()
        if not self.api_key:
            raise ValueError("TYPECAST_API_KEY가 비어 있습니다. GitHub Secrets를 확인해주세요.")
        
        masked = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "***"
        print(f"🔑 [Auth] TYPECAST_API_KEY 감지됨: {masked}")

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
                        print(f"🎯 필재 보이스 ID 발견: {v.get('voice_id')} ({name})")
                        return v.get("voice_id")
        except Exception as e:
            print(f"⚠️ 보이스 조회 경고: {e}")
        return "tc_61c0282465e94b8e88e14674" # 기본 필재 ID

    def synthesize(self, text: str, output_path: str, actor_id: str = None, tempo: float = 0.95):
        """
        공식 /v1/text-to-speech 엔드포인트로 바이너리 오디오 생성
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

        print(f"🎙️ [Typecast SSFM-V30] 요청 중 ({voice_id}): {text[:30]}...")
        
        response = requests.post(f"{self.BASE_URL}/v1/text-to-speech", headers=self.headers, json=payload)
        
        if response.status_code != 200:
            print(f"⚠️ Typecast API 응답 제한 ({response.status_code}): {response.text}")
            print("🎙️ 차분하고 지적인 다큐멘터리 낭독 보이스(Edge-TTS: InJoon)로 자동 전환하여 음성을 생성합니다...")
            return self._synthesize_fallback(text, output_path)

        # 정상 바이너리 WAV 오디오 저장
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"✅ [Typecast] 오디오 저장 완료: {output_path}")
        return output_path

    def _synthesize_fallback(self, text: str, output_path: str):
        """
        타입캐스트 제한 시 무료 고품질 한국어 다큐 보이스(InJoon)로 자동 합성
        """
        import asyncio
        import edge_tts

        async def _run():
            # ko-KR-InJoonNeural: 신뢰감 있고 차분한 남성 해설 보이스
            communicate = edge_tts.Communicate(text, "ko-KR-InJoonNeural", rate="-4%", pitch="-2Hz")
            await communicate.save(output_path)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        asyncio.run(_run())
        print(f"✅ [Fallback Voice] 고품질 낭독 오디오 저장 완료: {output_path}")
        return output_path

