from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field

from config.database import Base, Session, engine
from db import add
from jwt_manager import create_token, validate_token
from models.game import Game as GameModel
from models.game import Genre

app = FastAPI(title="App con FastAPI", version="0.0.1")
Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@email.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")


class User(BaseModel):
    email: str
    password: str


class Game(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=20)
    about: str = Field(min_length=5)
    realease_year: int = Field(le=2023)
    platform: str = Field(max_length=50)
    developer: str = Field(max_length=30)
    genre: str = Field(max_length=16)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Nombre del juego",
                "about": "El juego trata de:",
                "realease_year": 2023,
                "platform": "Plataforma",
                "developer": "Quien creo el juego",
                "genre": "Es un juego de:",
            }
        }


video_games = [
    {
        "id": 1,
        "name": "Disgaea",
        "about": "Tactical JRPG",
        "realease_year": 2003,
        "platform": "pc",
        "developer": "Nippon Ichi Software",
        "genre": "jrpg",
    },
    {
        "id": 2,
        "name": "Disgaea",
        "about": "Tactical JRPG",
        "realease_year": 2003,
        "platform": "switch",
        "developer": "Nippon Ichi Software",
        "genre": "tactis",
    },
]


@app.get("/", tags=["home"])
def main():
    return HTMLResponse("<h1>Hello World</h1>")


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@email.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)


@app.get(
    "/games",
    tags=["games"],
    response_model=List[Game],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_games():
    db = Session()
    res = db.query(GameModel).all()
    return JSONResponse(content=jsonable_encoder(res), status_code=200)


@app.get("/games/{id}", tags=["games"], response_model=Game)
def get_game(id: int = Path(ge=1)) -> Game:
    db = Session()
    res = db.query(GameModel).filter(GameModel.id == id).one_or_none()
    if res is None:
        return JSONResponse(status_code=404, content={"message": "game not found"})
    return JSONResponse(content=jsonable_encoder(res), status_code=200)


@app.get("/games/", tags=["games"], response_model=List[Game])
def get_game_by_genre(genre: str = Query(max_length=16)) -> List[Game]:
    db = Session()
    genre_id = db.query(Genre.id).filter(Genre.name == genre).one_or_none()
    if genre_id is None:
        return JSONResponse(content={"message": "Genre not exists"}, status_code=404)
    res = db.query(GameModel).filter(GameModel.genre == genre_id[0]).all()
    if not res:
        return JSONResponse(content={"message": "0 games"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(res), status_code=200)


@app.post("/games", tags=["games"], response_model=dict, status_code=201)
def create_game(game: Game) -> dict:
    db = Session()
    add.create_video_game(db, game)
    return JSONResponse(content={"message": "New video game saved"}, status_code=201)


@app.put("/games/{id}", tags=["games"], response_model=dict, status_code=200)
def update_game(id: int, game: Game) -> dict:
    for item in video_games:
        if item["id"] == id:
            item["name"] = game.name
            item["about"] = game.description
            item["realease_year"] = game.realease_year
            item["developer"] = game.developer
            item["genre"] = game.genre
            return JSONResponse(content={"message": "Game updated"}, status_code=200)


@app.delete("/games/{id}", tags=["games"], response_model=dict, status_code=200)
def delete_game(id: int) -> dict:
    for game in video_games:
        if game["id"] == id:
            video_games.remove(game)
            break
    return JSONResponse(content={"message": "Video game deleted"}, status_code=200)
