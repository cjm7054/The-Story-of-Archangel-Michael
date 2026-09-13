import os
import json
import subprocess
import requests
from PIL import Image, ImageOps

class VideoRenderer:
    """
    FFmpeg를 활용하여 Ken Burns(미세 줌 효과) + 자막 + 오디오 합성 렌더러
    """
    def __init__(self, width=1920, height=1080, fps=30):
        self.width = width
        self.height = height
        self.fps = fps

    def download_image(self, url: str, target_path: str):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                with open(target_path, "wb") as f:
                    f.write(res.content)
                
                # 16:9 비율에 맞춰 이미지 전처리 (리사이즈 및 중앙 크롭)
                img = Image.open(target_path).convert("RGB")
                img = ImageOps.fit(img, (self.width, self.height), Image.Resampling.LANCZOS)
                img.save(target_path, "JPEG", quality=95)
                return target_path
            else:
                print(f"⚠️ 이미지 다운로드 상태코드 ({res.status_code}): {url}")
        except Exception as e:
            print(f"⚠️ 이미지 다운로드 예외 발생: {e}")

        # 다운로드 실패 시 가톨릭 성당/기도 분위기의 딥 네이비 그라데이션 배경 이미지 자동 생성 (Fail-safe)
        print("🎨 고풍스러운 가톨릭 딥 네이비/골드 톤 배경으로 대체 생성합니다...")
        fallback_img = Image.new("RGB", (self.width, self.height), color=(15, 23, 42))
        fallback_img.save(target_path, "JPEG", quality=95)
        return target_path

    def get_audio_duration(self, audio_path: str) -> float:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", audio_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            return float(res.stdout.strip())
        except Exception:
            return 6.0 # 기본 fallback 6초

    def render_scene(self, image_path: str, audio_path: str, text: str, output_path: str, zoom_type: str = "zoom_in"):
        """
        단일 씬 렌더링 (Ken Burns 줌 효과 + 오디오 싱크 + 자막 오버레이)
        """
        duration = self.get_audio_duration(audio_path) + 0.5 # 0.5초 여운
        total_frames = int(duration * self.fps)

        # Ken Burns 필터 식 정의
        if zoom_type == "zoom_in":
            zoom_expr = f"zoompan=z='min(zoom+0.0008,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={self.width}x{self.height}:fps={self.fps}"
        elif zoom_type == "zoom_out":
            zoom_expr = f"zoompan=z='if(lte(zoom,1.0),1.25,max(1.0,zoom-0.0008))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={self.width}x{self.height}:fps={self.fps}"
        else:
            zoom_expr = f"zoompan=z='1.1':x='iw/2-(iw/zoom/2)+on*0.5':y='ih/2-(ih/zoom/2)':d={total_frames}:s={self.width}x{self.height}:fps={self.fps}"

        # 텍스트 줄바꿈 및 이스케이프 처리
        clean_text = text.replace("'", "").replace(":", "\\:")
        # 30자 단위로 줄바꿈
        lines = [clean_text[i:i+28] for i in range(0, len(clean_text), 28)]
        formatted_text = "\n".join(lines)

        drawtext_filter = (
            f"drawtext=text='{formatted_text}':"
            f"fontcolor=white:fontsize=48:line_spacing=20:"
            f"box=1:boxcolor=black@0.55:boxborderw=25:"
            f"x=(w-text_w)/2:y=h-text_h-100"
        )

        filter_complex = f"{zoom_expr},{drawtext_filter}"

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", image_path,
            "-i", audio_path,
            "-vf", filter_complex,
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            output_path
        ]

        print(f"🎬 씬 렌더링 시작 ({duration:.1f}초): {output_path}")
        subprocess.run(cmd, check=True)
        return output_path

    def concatenate_scenes(self, scene_video_paths: list, output_path: str):
        """
        각 씬 영상들을 하나의 최종 비디오로 병합
        """
        list_file = os.path.join(os.path.dirname(output_path), "concat_list.txt")
        with open(list_file, "w", encoding="utf-8") as f:
            for p in scene_video_paths:
                f.write(f"file '{os.path.abspath(p)}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_path
        ]
        print(f"🎞️ 전체 에피소드 병합 중: {output_path}")
        subprocess.run(cmd, check=True)
        return output_path
