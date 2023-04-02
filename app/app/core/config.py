import ipaddress

from pydantic import BaseSettings, PositiveInt


class Settings(BaseSettings):
    DEVEL_ENVIRONMENT: bool = False

    UVICORN_HOST: ipaddress.IPv4Address = "0.0.0.0"
    UVICORN_PORT: PositiveInt = 80
    UVICORN_RELOAD: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
