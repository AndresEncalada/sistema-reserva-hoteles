from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic leerá automáticamente estas variables desde el archivo .env
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instanciamos la configuración para usarla en toda la app
settings = Settings()