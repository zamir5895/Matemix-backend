from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from util import PyObjectId

class EjercicioResuelto(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    ejercicio_id: PyObjectId
    subtema_id: PyObjectId
    tema_id: PyObjectId
    alumno_id: int
    respuesta_usuario: str
    es_correcta: bool
    intentos: int = 0
    fecha_resuelto: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}