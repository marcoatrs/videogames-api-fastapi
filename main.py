from typing import Optional

from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="App con FastAPI", version="0.0.1")


class Game(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    realease_year: int
    developer: str
    genre: str


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


@app.get("/games", tags=["games"])
def get_games():
    return video_games


@app.get("/games/{id}", tags=["games"])
def get_game(id: int):
    for game in video_games:
        if game["id"] == id:
            return game
    return []


@app.get("/games/", tags=["games"])
def get_game_by_genre(genre: str):
    return [game for game in video_games if game["genre"] == genre]


@app.post("/games", tags=["games"])
def create_game(game: Game):
    video_games.append(game.model_dump())
    return game


@app.put("/games/{id}", tags=["games"])
def update_game(id: int, game: Game):
    for item in video_games:
        if item["id"] == id:
            item["name"] = game.name
            item["description"] = game.description
            item["realease_year"] = game.realease_year
            item["developer"] = game.developer
            item["genre"] = game.genre


@app.delete("/games/{id}", tags=["games"])
def delete_game(id: int):
    for game in video_games:
        if game["id"] == id:
            video_games.remove(game)
            break
    return video_games
