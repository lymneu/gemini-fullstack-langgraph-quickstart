import os
from dotenv import load_dotenv

# 在应用启动时加载 .env 文件
load_dotenv()

class Settings:
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_default_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()