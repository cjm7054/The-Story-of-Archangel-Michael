import os
import sys
import json
import argparse
from typecast_tts import TypecastTTS
from google_flow_visual import GoogleFlowVisual
from video_maker import VideoRenderer
from dotenv import load_dotenv

load_dotenv()

def generate_episode(episode_json_path: str, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = os.path.join(output_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    with open(episode_json_path, "r", encoding="utf-8") as f:
        ep_data = json.load(f)

    ep_id = ep_data.get("episode_id", "ep_default")
    scenes = ep_data.get("scenes", [])

    print(f"==================================================")
    print(f"🌟 [미카엘 가톨릭 지식 다큐 파이프라인] 가동")
    print(f"🎬 에피소드: {ep_data.get('title')}")
    print(f"총 {len(scenes)}개 씬 고품질 제작 시작")
    print(f"==================================================")

    tts = TypecastTTS()
    visual_gen = GoogleFlowVisual()
    renderer = VideoRenderer()

    scene_videos = []

    for idx, scene in enumerate(scenes):
        s_id = scene.get("scene_id", idx + 1)
        text = scene.get("text")
        prompt = scene.get("visual_prompt", "")
        fallback_url = scene.get("fallback_url")
        zoom = scene.get("zoom_effect", "zoom_in")

        audio_path = os.path.join(temp_dir, f"{ep_id}_scene_{s_id}.wav")
        img_path = os.path.join(temp_dir, f"{ep_id}_scene_{s_id}.jpg")
        scene_mp4 = os.path.join(temp_dir, f"{ep_id}_scene_{s_id}.mp4")

        print(f"\n--- [Scene {s_id}/{len(scenes)}] 제작 중 ---")

        # 1. 오디오: Typecast 필재 목소리 생성
        if not os.path.exists(audio_path):
            tts.synthesize(text, audio_path)

        # 2. 비주얼: Google Flow / Imagen 3 AI 시네마틱 이미지 생성 (또는 공인 명화 로드)
        if not os.path.exists(img_path):
            visual_gen.generate_image(prompt, img_path, fallback_url=fallback_url)

        # 3. 비디오 렌더링: Ken Burns 줌 모션 + 나눔명조 방송용 자막 바
        renderer.render_scene(img_path, audio_path, text, scene_mp4, zoom_type=zoom)
        scene_videos.append(scene_mp4)

    # 4. 전체 비디오 병합
    final_output = os.path.join(output_dir, f"{ep_id}_final.mp4")
    renderer.concatenate_scenes(scene_videos, final_output)

    print(f"\n==================================================")
    print(f"🎉 고품질 가톨릭 지식 다큐 영상 완성: {final_output}")
    print(f"==================================================")
    return final_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Catholic Auto Video Generator (Google Flow + Typecast)")
    parser.add_argument("--script", default="episodes/ep01_altar_kiss.json", help="Path to episode json")
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()

    generate_episode(args.script, args.output)
