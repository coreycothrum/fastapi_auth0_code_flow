from pydantic import BaseSettings, stricturl


class Settings(BaseSettings):
    AUTH0_DOMAIN: stricturl(allowed_schemes={"https"})  # noqa: F821
    AUTH0_AUDIENCE: stricturl(allowed_schemes={"https"})  # noqa: F821
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str

    AUTH0_ENDPOINT_PREFIX: str = "auth0"

    class Config:
        case_sensitive = True


settings = Settings()
