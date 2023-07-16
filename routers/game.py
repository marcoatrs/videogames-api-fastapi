from typing import List

from fastapi import APIRouter, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.game import Game as GameModel
from schemas.game import GameSchema
from services.game import GameService

game_router = APIRouter()


@game_router.get(
    "/games",
    tags=["games"],
    response_model=List[GameSchema],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_games():
    db = Session()
    res = GameService(db).get_games()
    return JSONResponse(content=jsonable_encoder(res), status_code=200)


@game_router.get("/games/{id}", tags=["games"], response_model=GameSchema)
def get_game(id: int = Path(ge=1)) -> GameSchema:
    db = Session()
    res = GameService(db).get_game(id)
    if res is None:
        return JSONResponse(status_code=404, content={"message": "game not found"})
    return JSONResponse(content=jsonable_encoder(res), status_code=200)


@game_router.get("/games/", tags=["games"], response_model=List[GameSchema])
def get_game_by_genre(genre: str = Query(max_length=16)) -> List[GameSchema]:
    db = Session()
    res = GameService(db).get_game_by_genre(genre)
    if res is None:
        return JSONResponse(content={"message": "Genre not exists"}, status_code=404)
    if not res:
        return JSONResponse(content={"message": "0 games"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(res), status_code=200)


@game_router.post("/games", tags=["games"], response_model=dict, status_code=201)
def create_game(game: GameSchema) -> dict:
    db = Session()
    GameService(db).create_game(game)
    return JSONResponse(content={"message": "New video game saved"}, status_code=201)


@game_router.put("/games/{id}", tags=["games"], response_model=dict, status_code=200)
def update_game(id: int, game: GameSchema) -> dict:
    db = Session()
    res = GameService(db).get_game(id)
    if res is None:
        return JSONResponse(content={"message": "Game not found"}, status_code=404)
    GameService(db).update_game(id, game)
    return JSONResponse(content={"message": "Game updated"}, status_code=200)


@game_router.delete("/games/{id}", tags=["games"], response_model=dict, status_code=200)
def delete_game(id: int) -> dict:
    db = Session()
    res = GameService(db).get_game(id)
    if res is None:
        return JSONResponse(content={"message": "Game not found"}, status_code=404)
    GameService(db).delete_game(id)
    return JSONResponse(content={"message": "Video game deleted"}, status_code=200)
