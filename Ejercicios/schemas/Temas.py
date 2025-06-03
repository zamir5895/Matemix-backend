from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum 
from util import PyObjectId

class NivelEnum(str, Enum):
    facil = "facil"
    medio = "medio"
    dificil = "dificil"

class EjercicioBase(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False 
    opciones: Optional[List[str]] = None
    respuesta_correcta: Optional[str] = None
    solucion: Optional[List[str]] = None
    pistas: Optional[List[str]] = None
    concepto_principal: Optional[str] = None
    nivel: NivelEnum


class YoutubeContentModel(BaseModel):
    url: Optional[str] = None


class SubtemaBase(BaseModel):
    titulo: str
    preguntas: Dict[NivelEnum, List[ObjectId]] = {}
    descripcion: Optional[str] = None
    video_id: Optional[List[PyObjectId]] = []

class TemaBase(BaseModel):
    nombre: str
    descripcion: str
    classroom_id:int
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