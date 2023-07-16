import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from schemas.auth import User
from utils.jwt_manager import create_token

auth_router = APIRouter()


@auth_router.post("/login", tags=["auth"])
def login(user: User):
    if (
        user.email == os.environ["ADMIN_EMAIL"]
        and user.password == os.environ["ADMIN_PASSWORD"]
    ):
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)
