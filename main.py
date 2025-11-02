# main.py
import os, json
from typing import Sequence, Mapping, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

# ---- SQLite 파일 경로(절대경로 고정: 어디서 실행해도 동일 DB 사용) ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "reviews.db")
print("[DB] Using SQLite:", DB_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

# 개발 기본값: true (운영 배포 시 false로 끄기)
SEED_ON_STARTUP = os.getenv("SEED_ON_STARTUP", "true").lower() == "true"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시 도메인으로 좁히기
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- DB 초기화/시드 로직 ----
def create_tables():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS reviews (
          review_id    TEXT PRIMARY KEY,
          global_score INTEGER NOT NULL,
          model_score  INTEGER NOT NULL,
          categories   TEXT NOT NULL,   -- JSON 문자열 저장
          summary      TEXT NOT NULL,
          created_at   TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """))

def is_empty() -> bool:
    with engine.connect() as conn:
        cnt = conn.execute(text("SELECT COUNT(*) FROM reviews")).scalar_one()
        return (cnt or 0) == 0

def seed_reviews():
    rows = [
        {
            "id": "v1",
            "g": 68, "m": 65,
            "c": json.dumps([
                {"name": "readability", "score": 70},
                {"name": "efficiency",  "score": 60},
                {"name": "consistency", "score": 75},
            ]),
            "s": "기본 구조는 괜찮지만 효율/일관성 개선 필요.",
        },
        {
            "id": "v2",
            "g": 94, "m": 91,
            "c": json.dumps([
                {"name": "readability", "score": 95},
                {"name": "efficiency",  "score": 90},
                {"name": "consistency", "score": 97},
            ]),
            "s": "탁월한 코드 품질. 유지보수 용이.",
        },
        {
            "id": "v3",
            "g": 45, "m": 40,
            "c": json.dumps([
                {"name": "readability", "score": 50},
                {"name": "efficiency",  "score": 30},
                {"name": "consistency", "score": 55},
            ]),
            "s": "리팩토링 권장. 가독성/효율 모두 낮음.",
        },
    ]
    insert_sql = text("""
      INSERT OR REPLACE INTO reviews
      (review_id, global_score, model_score, categories, summary)
      VALUES (:id, :g, :m, :c, :s)
    """)
    with engine.begin() as conn:
        conn.execute(insert_sql, rows)

# ---- 서버 시작 시 1회 실행 ----
@app.on_event("startup")
def startup_seed():
    create_tables()
    empty = is_empty()
    if SEED_ON_STARTUP and empty:
        seed_reviews()
        print("[startup] DB seeded with v1/v2/v3.")
    else:
        print(f"[startup] seed skipped. SEED_ON_STARTUP={SEED_ON_STARTUP}, empty={empty}")

# ---- API ----
@app.get("/review/{review_id}")
def get_review(review_id: str):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT review_id, global_score, model_score, categories, summary
                FROM reviews
                WHERE review_id = :rid
            """),
            {"rid": review_id},
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        cats = json.loads(row.categories) if isinstance(row.categories, str) else row.categories
        return {
            "review_id": row.review_id,
            "global_score": row.global_score,
            "model_score": row.model_score,
            "categories": cats,
            "summary": row.summary,
        }

@app.get("/reviews")
def list_reviews(limit: int = 10):
    with engine.connect() as conn:
        rows: Sequence[Mapping[str, Any]] = conn.execute(
            text("""
              SELECT review_id, global_score, model_score, categories, summary
              FROM reviews
              ORDER BY created_at DESC
              LIMIT :limit
            """),
            {"limit": limit},
        ).mappings().all()

        return {"items": [
            {
                "review_id": r["review_id"],
                "global_score": r["global_score"],
                "model_score": r["model_score"],
                "categories": json.loads(r["categories"]),
                "summary": r["summary"],
            } for r in rows
        ]}
