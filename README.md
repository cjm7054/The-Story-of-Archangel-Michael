# 미카엘이 전하는 가톨릭이야기 - 자동화 영상 생성 시스템

'신비한 건축사전' 스타일처럼 **정갈한 고화질 성화/사진 + 젠틀한 줌인(Ken Burns) 효과 + 타입캐스트 '필재' 목소리 해설 + 깔끔한 자막**을 결합하여 자동으로 유튜브 영상을 생성하는 깃허브 기반 자동화 파이프라인입니다.

---

## 📂 프로젝트 구조

```text
미카엘이 전하는 가톨릭이야기/
├── .github/
│   └── workflows/
│       └── generate_video.yml     # 깃허브 액션 영상 자동 빌드 워크플로우
├── src/
│   ├── typecast_tts.py            # 타입캐스트(필재) API 연동 음성 합성기
│   ├── video_maker.py             # FFmpeg Ken Burns 줌 효과 및 자막 합성 엔진
│   └── main.py                    # 에피소드 실행 메인 파이프라인
├── episodes/
│   └── ep01_altar_kiss.json       # 제1화: 사제는 왜 제대에 입을 맞출까? (샘플)
├── .env                           # 로컬 API 키 (Git 제외)
├── .gitignore                     # 보안 및 대용량 파일 제외 설정
├── requirements.txt               # 파이썬 의존성
└── channel_branding_guide.md      # 채널 브랜딩 및 톤앤매너 가이드
```

---

## 🚀 깃허브(GitHub) 자동 생성 사용법

### 1. 깃허브 Secret 설정 (최초 1회)
1. 생성하신 GitHub 저장소의 **Settings** -> **Secrets and variables** -> **Actions** 메뉴로 이동합니다.
2. **New repository secret** 버튼 클릭:
   * **Name**: `TYPECAST_API_KEY`
   * **Secret**: 발급받으신 타입캐스트 API Key 붙여넣기

### 2. 영상 원클릭 생성 실행
1. 깃허브 저장소의 **Actions** 탭으로 이동합니다.
2. 좌측 메뉴에서 **Generate Catholic Video** 워크플로우를 선택합니다.
3. 우측 **Run workflow** 드롭다운 버튼을 클릭하고 `Run workflow`를 누릅니다.
   * 기본값으로 `episodes/ep01_altar_kiss.json`이 실행됩니다.
4. 약 1~3분 뒤 작업이 완료되면, **Artifacts** 섹션에서 완성된 `catholic-video-output` (`.mp4`) 파일을 즉시 다운로드하실 수 있습니다!

---

## ✍️ 새로운 에피소드 추가하는 방법

`episodes/` 폴더에 새로운 JSON 파일(예: `ep02_christmas_history.json`)을 만들어 씬별로 대본과 이미지 링크만 적어주시면 됩니다:

```json
{
  "episode_id": "ep02_advent_candle",
  "title": "대림초 색깔에 숨겨진 보라색과 분홍색의 비밀",
  "scenes": [
    {
      "scene_id": 1,
      "text": "대림 시기가 되면 제대 앞에는 네 개의 초가 켜집니다. 그런데 왜 보라색 초 세 개와 분홍색 초 하나일까요?",
      "image_url": "https://고화질_이미지_주소.jpg",
      "zoom_effect": "zoom_in"
    }
  ]
}
```
* `zoom_effect`: `zoom_in`(서서히 확대), `zoom_out`(서서히 축소), `pan_right`(부드러운 이동) 지원.
