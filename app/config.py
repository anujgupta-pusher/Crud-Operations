
import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@:5432/dbname")