import os

JWT_SECRET = os.getenv("JWT_SECRET") or ""
DB_URI = os.getenv("DB_URI") or ""
