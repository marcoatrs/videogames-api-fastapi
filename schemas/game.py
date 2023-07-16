from typing import Optional

from pydantic import BaseModel, Field


class GameSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=20)
    about: str = Field(min_length=5)
    realease_year: int = Field(le=2023)
    platform: str = Field(max_length=50)
    developer: str = Field(max_length=30)
    genre: str = Field(max_length=16)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Nombre_del_juego",
                "about": "El_juego_trata_de",
                "realease_year": 2023,
                "platform": "Plataforma",
                "developer": "Quien_creo_el_juego",
                "genre": "Es_un_juego_de",
            }
        }