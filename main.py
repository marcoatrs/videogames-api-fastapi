from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="App con FastAPI", version="0.0.1")

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
