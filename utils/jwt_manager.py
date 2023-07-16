import os

from dotenv import load_dotenv
from jwt import decode, encode

load_dotenv()


def create_token(data: dict) -> str:
    return encode(
        payload=data,
        key=os.environ.get("SECRET_KEY", "my_secret_key"),
        algorithm="HS256",
    )


def validate_token(token: str) -> dict:
    return decode(
        jwt=token,
        key=os.environ.get("SECRET_KEY", "my_secret_key"),
        algorithms=["HS256"],
    )
