# health-trend-dashboard

건강기능식품 시장 트렌드 대시보드 — 일일 리포트를 쌓아 주간·월간으로 이어 가는 누적형 정적 사이트입니다.

- 공개 페이지: https://kshan96-hue.github.io/health-trend-dashboard/
- 렌더러: `index.html` (HTML·CSS·바닐라 JS 단일 파일, 외부 CDN 없음)
- 데이터: `data/` 아래 JSON (일일/주간/월간)
- 빌드 도구: `tools/template.html` + `tools/build.py`

## 데이터 누적 구조

```
data/
  manifest.json              ← 어떤 리포트가 있는지 목록
  daily/2026-11-25.json      ← 날짜별 일일 리포트 (덮어쓰지 않고 하루 한 파일)
  weekly/2026-W48.json       ← 주간 리포트 (첫 리포트 2026-11-30 예정)
  monthly/2026-11.json       ← 월간 리포트 (첫 리포트 2026-12-01 예정)
```

`data/manifest.json` 형식:

```json
{ "daily": ["2026-11-25"], "weekly": [], "monthly": [] }
```

- 새 날짜 파일을 `data/daily/`에 추가하고 `manifest.json`의 `daily` 배열에 날짜를 넣으면, 대시보드의 날짜 드롭다운·이전/다음 버튼에 자동으로 나타납니다.
- `weekly`·`monthly` 배열에 항목이 생기면 주간/월간 탭이 그 리포트를 렌더링합니다. 아직 데이터가 없을 때는 가짜 데이터를 넣지 않고 "매주 월요일 / 매월 1일 자동 생성" 안내 상태를 보여 줍니다.
- 일일 리포트 화면의 **누적 추이(히스토리 비교)** 영역은 `daily`가 2일 이상이면 전일 대비 KPI·검색어 순위·상품 순위 변동을 자동 계산합니다. 1일차에는 "1일차 기준 데이터 저장 완료" 안내만 표시합니다.

## 열리는 방식

- 웹(HTTPS): `fetch('./data/manifest.json')`과 선택한 리포트 JSON(`data/daily/YYYY-MM-DD.json`)을 불러와 렌더링합니다.
- 로컬(`file://`): `fetch`가 막히면 `index.html`에 내장된 최신 일일 JSON으로 대체합니다. `tools/build.py`가 최신 일일 리포트와 manifest를 `index.html`에 심습니다.

## 갱신 절차

1. `data/daily/YYYY-MM-DD.json` 작성 — `views.summary/market/youtube/rank` 블록 구조와 `trend`(KPI·키워드·상품 순위 스냅샷)를 채웁니다.
2. `data/manifest.json`의 `daily` 배열에 날짜 추가.
3. `python3 tools/build.py` — `tools/template.html`에 최신 데이터를 심어 `index.html` 생성.
4. `git push origin main` 및 `git push origin main:gh-pages` — GitHub Pages 소스는 `gh-pages` 브랜치 `/(root)`.

## 내용 기준

- 2026-11-25 1회차 브리핑 데이터 기준. 시장·규제·채널·제형·검색·커머스 랭킹을 한 장에 정리.
- 확인하지 못한 항목은 '미확인', 해석이 들어간 부분은 '해석'·'추정'으로 구분.
- **제형 균형**: 정제·캡슐·분말·스틱·액상·음료·구미를 같은 무게로 다룹니다. 채널 성장률(예: 올리브영 자체브랜드 구미 +280%)은 사실 그대로 두되, 이를 특정 제형 우위로 해석하지 않습니다. 제형별 국내 시장 규모는 미확인입니다.
- **아하핏 적합함 렌즈**: `ahai.co.kr`의 "적합함(Aha! + fit)" — 적합한 품질·적합한 기능·적합한 가격을 MD 시사점과 기회 후보의 판단 기준으로 씁니다. 공개 저장소이므로 개인정보·비공개 기획안은 넣지 않습니다.
- `<meta name="robots" content="noindex,nofollow">` 유지.
