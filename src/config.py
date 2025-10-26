from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str
    
    # JWT configuration  
    JWT_ALGORITHM: str = "HS256"
    SECRET_KEY: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()