from typing import List, Optional

from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from jwt_manager import create_token

app = FastAPI(title="App con FastAPI", version="0.0.1")


class User(BaseModel):
    email: str
    password: str


class Game(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=20)
    description: str = Field(min_length=5)
    realease_year: int = Field(le=2023)
    developer: str = Field(max_length=30)
    genre: str = Field(max_length=16)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Nombre del juego",
                "description": "El juego trata de:",
                "realease_year": 2023,
                "developer": "Quien creo el juego",
                "genre": "Es un juego de:",
            }
        }


video_games = [
    {
        "id": 1,
        "name": "Disgaea",
        "description": "Tactical JRPG",
        "realease_year": 2003,
        "developer": "Nippon Ichi Software",
        "genre": "jrpg",
    },
    {
        "id": 2,
        "name": "Disgaea",
        "description": "Tactical JRPG",
        "realease_year": 2003,
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


@app.get("/games", tags=["games"], response_model=List[Game], status_code=200)
def get_games() -> List[Game]:
    return JSONResponse(content=video_games, status_code=200)


@app.get("/games/{id}", tags=["games"], response_model=Game)
def get_game(id: int = Path(ge=1)) -> Game:
    for game in video_games:
        if game["id"] == id:
            return JSONResponse(content=game)
    return JSONResponse(content=[], status_code=404)


@app.get("/games/", tags=["games"], response_model=List[Game])
def get_game_by_genre(genre: str = Query(max_length=16)) -> List[Game]:
    res = [game for game in video_games if game["genre"] == genre]
    return JSONResponse(content=res)


@app.post("/games", tags=["games"], response_model=dict, status_code=201)
def create_game(game: Game) -> dict:
    video_games.append(game.model_dump())
    return JSONResponse(content={"message": "New video game saved"}, status_code=201)


@app.put("/games/{id}", tags=["games"], response_model=dict, status_code=200)
def update_game(id: int, game: Game) -> dict:
    for item in video_games:
        if item["id"] == id:
            item["name"] = game.name
            item["description"] = game.description
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
