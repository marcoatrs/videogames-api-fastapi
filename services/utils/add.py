from sqlalchemy.orm import Session

from models.game import Developer
from models.game import Game as GameModel
from models.game import Genre, Platform
from schemas.game import GameSchema


def get_platform(db: Session, game: GameSchema) -> int:
    platform_id: int = (
        db.query(Platform.id).filter(Platform.name == game.platform).one_or_none()
    )
    if platform_id is None:
        new_platform = Platform(name=game.platform)
        db.add(new_platform)
        db.commit()
        return new_platform.id
    return platform_id[0]


def get_genre(db: Session, game: GameSchema) -> int:
    genre_id: int = db.query(Genre.id).filter(Genre.name == game.genre).one_or_none()
    if genre_id is None:
        new_genre = Genre(name=game.genre)
        db.add(new_genre)
        db.commit()
        return new_genre.id
    return genre_id[0]


def get_developer(db: Session, game: GameSchema) -> int:
    developer_id: int = (
        db.query(Developer.id).filter(Developer.name == game.developer).one_or_none()
    )
    if developer_id is None:
        new_dev = Developer(name=game.developer)
        db.add(new_dev)
        db.commit()
        return new_dev.id
    return developer_id[0]


def create_video_game(db: Session, game: GameSchema):
    # Platform
    platform_id = get_platform(db, game)

    # Genre
    genre_id = get_genre(db, game)

    # Developer
    developer_id = get_developer(db, game)

    game_dict = game.model_dump()

    new_game = GameModel(
        name=game_dict["name"],
        platform=platform_id,
        genre=genre_id,
        developer=developer_id,
        realease_year=game_dict["realease_year"],
        about=game_dict["about"],
    )
    db.add(new_game)
    db.commit()
