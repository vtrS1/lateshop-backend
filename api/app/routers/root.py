from fastapi.routing import APIRouter
from fastapi import Depends

from app.config.environment import Settings, get_settings

router = APIRouter(tags=["root"])


@router.get("/")
def root(env: Settings = Depends(get_settings)):
    return {
        "message": "Welcome to Latesjop's API",
        "version": "0.1.0",
        "docs": "/docs",
        "environment": env.environment,
        "testing": env.testing,
    }
