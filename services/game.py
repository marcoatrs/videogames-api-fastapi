from typing import List

from sqlalchemy.orm import Session
from models.game import Game as GameModel
from models.game import Genre
from schemas.game import GameSchema

from .utils import add

class GameService:
    def __init__(self, db: Session):
        self.db = db

    def get_games(self):
        return self.db.query(GameModel).all()

    def get_game(self, id: int):
        return self.db.query(GameModel).filter(GameModel.id == id).first()

    def get_game_by_genre(self, genre: str) -> List[GameModel] | None:
        genre_id = self.db.query(Genre.id).filter(Genre.name == genre).one_or_none()
        if genre_id is None:
            return None
        return self.db.query(GameModel).filter(GameModel.genre == genre_id[0]).all()

    def create_game(self, game: GameSchema):
        add.create_video_game(self.db, game)

    def update_game(self, id: int, game: GameSchema):
        res = self.get_game(id)
        res.name = game.name
        res.about = game.about
        res.realease_year = game.realease_year
        res.platform = add.get_platform(self.db, game)
        res.developer = add.get_developer(self.db, game)
        res.genre = add.get_genre(self.db, game)
        self.db.commit()

    def delete_game(self, id: int):
        game = self.get_game(id)
        self.db.delete(game)
        self.db.commit()