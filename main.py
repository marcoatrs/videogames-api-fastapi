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
    }
]


@app.get("/", tags=["home"])
def main():
    return HTMLResponse("<h1>Hello World</h1>")


@app.get("/games", tags=["games"])
def get_games():
    return video_games
