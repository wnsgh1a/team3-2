# 🧩 프로젝트 개요: FastAPI + SQLite + Next.js 결과 조회 시스템

이 프로젝트는 **AI 코드 평가 결과**를  
“DB → FastAPI → Next.js” 흐름으로 조회하는 시스템입니다.

---

## 🚀 현재까지 진행 상황 요약

### 1️⃣ 백엔드 (FastAPI)

-   **SQLite 데이터베이스 연결 완료**
-   서버 시작 시 자동으로 DB 초기화 및 시드(`v1`, `v2`, `v3`)
-   `/review/{id}`: 단일 리뷰 데이터 조회 API
-   `/reviews`: 최근 리뷰 목록 조회 API
-   FastAPI 실행 시 콘솔에 DB 경로와 시드 로그 표시

> ✅ 별도 `init_db.py` 실행이 필요 없음  
> 서버가 켜질 때 자동으로 테이블 생성 + 샘플 데이터 삽입

---

### 2️⃣ 데이터베이스 구조 (`reviews.db`)

| 컬럼명         | 타입       | 설명                          |
| -------------- | ---------- | ----------------------------- |
| `review_id`    | TEXT (PK)  | 리뷰 ID (`v1`, `v2`, `v3` 등) |
| `global_score` | INTEGER    | 전체 점수                     |
| `model_score`  | INTEGER    | 모델별 점수                   |
| `categories`   | TEXT(JSON) | 카테고리별 점수 (JSON 문자열) |
| `summary`      | TEXT       | 간단한 요약                   |
| `created_at`   | TEXT       | 생성 시각 (자동 입력)         |

샘플 데이터 예시:

```json
{
  "review_id": "v1",
  "global_score": 68,
  "model_score": 65,
  "categories": [
    { "name": "readability", "score": 70 },
    { "name": "efficiency", "score": 60 },
    { "name": "consistency", "score": 75 }
  ],
  "summary": "기본 구조는 괜찮지만 효율/일관성 개선 필요."
}
```

###3️⃣ 프론트엔드 (Next.js)
.env.local 파일에 FastAPI 서버 주소 설정:

ini
코드 복사
API_BASE=http://localhost:8000
/review/[id] 페이지에서 FastAPI API 호출

응답(global_score, categories, summary)을 시각화 및 표시

⚙️ 실행 방법
🐍 1. FastAPI 서버 실행
bash
코드 복사
# FastAPI 실행 (main.py가 있는 경로에서)
uvicorn main:app --reload --port 8000
실행 후 콘솔 로그 예시:

csharp
코드 복사
[DB] Using SQLite: C:\Users\wnsgh\Desktop\team3\reviews.db
[startup] DB seeded with v1/v2/v3.
http://localhost:8000/reviews → 리뷰 목록 확인

http://localhost:8000/review/v1 → 단일 리뷰 JSON 확인

⚡ 2. Next.js 프론트 실행
bash
코드 복사
# team3 폴더에서
npm run dev
실행 후:

로컬 주소: http://localhost:3000

테스트 페이지:

http://localhost:3000/review/v1

http://localhost:3000/review/v2

http://localhost:3000/review/v3

🔍 확인 체크리스트
항목	정상 상태
reviews.db 파일	프로젝트 루트에 존재해야 함
/reviews API	v1, v2, v3 데이터가 JSON으로 출력
/review/v1	단일 리뷰 JSON 확인 가능
Next.js	/review/v1 페이지에서 점수와 요약이 표시됨
콘솔 로그	[startup] DB seeded with v1/v2/v3. 출력

🧠 구조 요약
scss
코드 복사
┌───────────────┐        ┌────────────┐        ┌──────────────┐
│   SQLite DB   │ ───▶   │  FastAPI   │ ───▶   │  Next.js UI  │
│ (reviews.db)  │        │  (API)     │        │ (프론트엔드) │
└───────────────┘        └────────────┘        └──────────────┘
        ▲                      ▲                      │
        │ 자동 초기화(시드)     │ JSON 응답             │ 시각화 및 표시
        └──────────────────────────────────────────────┘
🛠️ 환경 변수 요약
변수명	기본값	설명
SEED_ON_STARTUP	true	서버 시작 시 자동 시드 여부
API_BASE	http://localhost:8000	Next.js에서 FastAPI 호출 주소

🧩 향후 확장 계획
POST /review — AI가 분석한 새 리뷰를 DB에 업서트

/reviews — 필터, 정렬, 검색 기능 추가

DB 전환: SQLite → Supabase(PostgreSQL)

그래프 시각화: 점수 히스토리 및 평균 점수 추적

💡 정리:
FastAPI 서버를 켜면 DB가 자동으로 준비되고,
Next.js 페이지에서 즉시 v1~v3 결과를 시각적으로 확인할 수 있습니다.
```
