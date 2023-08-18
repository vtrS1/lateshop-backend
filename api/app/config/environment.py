import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "development"
    testing: bool = False
    database_url: AnyUrl
    database_url_test: AnyUrl

    jwt_secretkey: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int



    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    log.info("Loading settings from environment ...")
    return Settings()
