from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        extra = 'ignore'
        env_file = '.env'


settings = Settings()
