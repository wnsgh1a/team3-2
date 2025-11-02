import os, json
from sqlalchemy import create_engine, text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "reviews.db")
print("Init SQLite DB:", DB_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True, future=True)

with engine.begin() as conn:
    # 테이블 생성
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS reviews (
      review_id   TEXT PRIMARY KEY,
      global_score INTEGER NOT NULL,
      model_score  INTEGER NOT NULL,
      categories   TEXT NOT NULL,   -- JSON 문자열 저장
      summary      TEXT NOT NULL,
      created_at   TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """))

    # 안전한 executemany: 값은 전부 바인딩으로 전달
    insert_sql = text("""
      INSERT OR REPLACE INTO reviews
      (review_id, global_score, model_score, categories, summary)
      VALUES (:id, :g, :m, :c, :s)
    """)

    rows = [
        {
            "id": "v1",
            "g": 68,
            "m": 65,
            "c": json.dumps([
                {"name": "readability", "score": 70},
                {"name": "efficiency",  "score": 60},
                {"name": "consistency", "score": 75},
            ]),
            "s": "기본 구조는 괜찮지만 효율/일관성 개선 필요.",
        },
        {
            "id": "v2",
            "g": 94,
            "m": 91,
            "c": json.dumps([
                {"name": "readability", "score": 95},
                {"name": "efficiency",  "score": 90},
                {"name": "consistency", "score": 97},
            ]),
            "s": "탁월한 코드 품질. 유지보수 용이.",
        },
        {
            "id": "v3",
            "g": 45,
            "m": 40,
            "c": json.dumps([
                {"name": "readability", "score": 50},
                {"name": "efficiency",  "score": 30},
                {"name": "consistency", "score": 55},
            ]),
            "s": "리팩토링 권장. 가독성/효율 모두 낮음.",
        },
    ]

    conn.execute(insert_sql, rows)

print("SQLite 초기화 완료 ✅  (v1/v2/v3 업서트)")
