import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    # defaults
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

    # server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        if missing:
            raise EnvironmentError(f"missing: {', '.join(missing)}")
        return True


settings = Settings()
