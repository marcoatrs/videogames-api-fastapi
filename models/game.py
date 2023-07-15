from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Platform(Base):
    __tablename__ = "platforms"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String)
    games: Mapped[List["Game"]] = relationship()


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String)
    games: Mapped[List["Game"]] = relationship()


class Developer(Base):
    __tablename__ = "developers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String)
    games: Mapped[List["Game"]] = relationship()


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    platform: Mapped[int] = mapped_column(ForeignKey("platforms.id"))
    genre: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    realease_year = Column(Integer)
    about = Column(Text)
