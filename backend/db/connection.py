# ✅ /backend/db/connection.py

import os
from dotenv import load_dotenv
import psycopg2

# 🔄 Load environment variables from .env
load_dotenv()

# 🧠 Connection config (from .env)
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD", ""),  # fallback to blank
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# ✅ Optional: test the connection when run directly
if __name__ == "__main__":
    try:
        conn = get_conn()
        print("✅ Connected to Postgres!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)
