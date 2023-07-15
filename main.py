from typing import List, Optional

from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="App con FastAPI", version="0.0.1")


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


@app.get("/games", tags=["games"], response_model=List[Game])
def get_games() -> List[Game]:
    return JSONResponse(content=video_games)


@app.get("/games/{id}", tags=["games"], response_model=Game)
def get_game(id: int = Path(ge=1)) -> Game:
    for game in video_games:
        if game["id"] == id:
            return JSONResponse(content=game)
    return JSONResponse(content=[])


@app.get("/games/", tags=["games"], response_model=List[Game])
def get_game_by_genre(genre: str = Query(max_length=16)) -> List[Game]:
    res = [game for game in video_games if game["genre"] == genre]
    return JSONResponse(content=res)


@app.post("/games", tags=["games"], response_model=dict)
def create_game(game: Game) -> dict:
    video_games.append(game.model_dump())
    return JSONResponse(content={"message": "New video game saved"})


@app.put("/games/{id}", tags=["games"], response_model=dict)
def update_game(id: int, game: Game) -> dict:
    for item in video_games:
        if item["id"] == id:
            item["name"] = game.name
            item["description"] = game.description
            item["realease_year"] = game.realease_year
            item["developer"] = game.developer
            item["genre"] = game.genre
            return JSONResponse(content={"message": "Game updated"})


@app.delete("/games/{id}", tags=["games"], response_model=dict)
def delete_game(id: int) -> dict:
    for game in video_games:
        if game["id"] == id:
            video_games.remove(game)
            break
    return JSONResponse(content={"message": "Video game deleted"})
