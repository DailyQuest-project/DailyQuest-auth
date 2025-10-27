from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    
    JWT_ALGORITHM: str = "HS256"
    SECRET_KEY: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()