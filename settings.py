from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    S3_URL: str
    S3_REGION: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_FILE_PREFIX: str
    S3_BUCKET_NAME: str

    class Config:
        extra = 'ignore'
        env_file = '.env'


settings = Settings()
