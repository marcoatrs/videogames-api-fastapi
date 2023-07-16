from typing import List, Optional

from fastapi import Depends, FastAPI, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from config.database import Base, Session, engine
from db import add
from jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from models.game import Game as GameModel
from models.game import Genre

app = FastAPI(title="App con FastAPI", version="0.0.1")
app.add_middleware(ErrorHandler)
Base.metadata.create_all(bind=engine)


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
    db = Session()
    res = db.query(GameModel).filter(GameModel.id == id).first()
    if res is None:
        return JSONResponse(content={"message": "Game not found"}, status_code=404)
    res.name = game.name
    res.about = game.about
    res.realease_year = game.realease_year
    res.platform = add.get_platform(db, game)
    res.developer = add.get_developer(db, game)
    res.genre = add.get_genre(db, game)
    db.commit()
    return JSONResponse(content={"message": "Game updated"}, status_code=200)


@app.delete("/games/{id}", tags=["games"], response_model=dict, status_code=200)
def delete_game(id: int) -> dict:
    db = Session()
    res = db.query(GameModel).filter(GameModel.id == id).first()
    if res is None:
        return JSONResponse(content={"message": "Game not found"}, status_code=404)
    db.delete(res)
    db.commit()
    return JSONResponse(content={"message": "Video game deleted"}, status_code=200)
