from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Padrão comum para URL de conexão com o banco de dados.
    # Removido o valor padrão para forçar a configuração via .env ou variáveis de ambiente.
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()