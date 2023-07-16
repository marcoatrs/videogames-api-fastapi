from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.game import Developer
from models.game import Game as GameModel
from models.game import Genre, Platform


def create_video_game(db: Session, game: BaseModel):
    # Platform
    platform_id: int = (
        db.query(Platform.id).filter(Platform.name == game.platform).one_or_none()
    )
    if platform_id is None:
        new_platform = Platform(name=game.platform)
        db.add(new_platform)
        db.commit()
        platform_id = [new_platform.id]

    # Genre
    genre_id: int = db.query(Genre.id).filter(Genre.name == game.genre).one_or_none()
    if genre_id is None:
        new_genre = Genre(name=game.genre)
        db.add(new_genre)
        db.commit()
        genre_id = [new_genre.id]

    # Developer
    developer_id: int = (
        db.query(Developer.id).filter(Developer.name == game.developer).one_or_none()
    )
    if developer_id is None:
        new_dev = Developer(name=game.developer)
        db.add(new_dev)
        db.commit()
        developer_id = [new_dev.id]

    game_dict = game.model_dump()

    new_game = GameModel(
        name=game_dict["name"],
        platform=platform_id[0],
        genre=genre_id[0],
        developer=developer_id[0],
        realease_year=game_dict["realease_year"],
        about=game_dict["about"],
    )
    db.add(new_game)
    db.commit()
