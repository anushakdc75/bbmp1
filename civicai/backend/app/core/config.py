from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CivicAI"
    env: str = "dev"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./civicai.db"
    redis_url: str = "redis://redis:6379/0"
    model_store: str = "./models"
    data_file: str = "../data/bbmp_reddit_data.csv"
    rate_limit: str = "60/minute"

    class Config:
        env_file = ".env"


settings = Settings()
