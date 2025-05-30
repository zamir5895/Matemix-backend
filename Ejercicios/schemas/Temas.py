from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum 
from util import PyObjectId

class EjercicioBase(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False 
    opciones: Optional[List[str]] = None
    respuesta: Optional[str] = None
    solucion: Optional[List[str]] = None
    pistas: Optional[List[str]] = None
    concepto_principal: Optional[str] = None

class NivelEnum(str, Enum):
    facil = "facil"
    medio = "medio"
    dificil = "dificil"

class YoutubeContentModel(BaseModel):
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None


class SubtemaBase(BaseModel):
    nivel: NivelEnum
    titulo: str
    preguntas: List[EjercicioBase]
    descripcion: Optional[str] = None
    video_id: Optional[List[PyObjectId]] = None

class TemaBase(BaseModel):
    nombre: str
    descripcion: str
    subtema_id: Optional[List[PyObjectId]] = None

class TemaCreate(TemaBase):
    pass

class SubtemaCreate(SubtemaBase):
    pass

class EjercicioCreate(EjercicioBase):
    pass
class Ejercicio(EjercicioBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



class Subtema(SubtemaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Tema(TemaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}