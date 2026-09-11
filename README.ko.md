# Koi StyleKit

[简体中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | **한국어** | [Español](README.es.md)

Koi StyleKit은 손그림 일러스트 스타일을 탐색하고 재사용 가능한 프롬프트 레시피를 내보내는 오픈 소스 로컬 도구입니다.

## 주요 기능

- 48개 스타일 패밀리와 300개 이상의 레시피 검색·필터·비교
- 샘플 이미지와 검증 상태 확인
- 중국어 프롬프트와 JSON 스타일 패키지 내보내기
- Python CLI 또는 로컬 웹 갤러리로 사용

## 온라인 체험

[갤러리 열기](https://www.starshoreai.com/koi-stylekit/gallery/). 다운로드나 Python 설치 없이 308개 레시피(48개 패밀리와 260개 변형)를 탐색하고 프롬프트를 내보낼 수 있습니다. 이미지를 자동 생성하지 않으며 주제는 서버에 전송되지 않습니다. 문서는 5개 언어로 제공되지만 UI와 프롬프트는 주로 중국어입니다.

## 로컬 실행

```sh
git clone https://github.com/koi-lee/koi-stylekit.git
cd koi-stylekit
python3 scripts/serve.py
```

브라우저에서 `http://127.0.0.1:4317/`을 여세요. 이미지 생성 API를 호출하지 않으며 주제는 외부로 전송되지 않습니다.

샘플 이미지는 단일 주제로 생성한 후보이며 다른 주제나 모델에서의 재현을 보장하지 않습니다. 자세한 내용은 [README.md](README.md)와 [기계 판독 요약](wireframes/llms.txt)을 확인하세요.
