from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.auth import auth_router
from routers.game import game_router

app = FastAPI(title="App con FastAPI", version="0.0.1")
app.add_middleware(ErrorHandler)
app.include_router(auth_router)
app.include_router(game_router)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["home"])
def main():
    return HTMLResponse("<h1>Hello World</h1>")
