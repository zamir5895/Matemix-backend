# Clase para poner los dto para los temas y subtemas

from pydantic import BaseModel, Field



class CreateTema(BaseModel):
    nombre: str
    descripcion: str
    classroom_id: int
    subtema_id: list[str] = Field(default_factory=list)


