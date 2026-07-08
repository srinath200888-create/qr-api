from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "QR Code API"
    debug: bool = False
    rate_limit_enabled: bool = True
    rate_limit_redis_url: str | None = None
    rapidapi_secret: str = ""
    rapidapi_enabled: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
