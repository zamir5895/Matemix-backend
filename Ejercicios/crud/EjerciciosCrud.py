from fastapi import APIRouter, HTTPException
from services.EjerciciosService import EjercicioService
from schemas.Temas import Ejercicio, EjercicioCreate

router = APIRouter()

@router.post("/", response_model=str)
async def create(ejercicio: EjercicioCreate):
    return await EjercicioService.create_ejercicio(ejercicio)

@router.get("/{ejercicio_id}", response_model=Ejercicio)
async def get(ejercicio_id: str):
    ejercicio = await EjercicioService.get_ejercicio_by_id(ejercicio_id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return ejercicio

@router.put("/{ejercicio_id}")
async def update(ejercicio_id: str, ejercicio: EjercicioCreate):
    await EjercicioService.update_ejercicio(ejercicio_id, ejercicio)
    return {"mensaje": "Ejercicio actualizado correctamente"}

@router.delete("/{ejercicio_id}")
async def delete(ejercicio_id: str):
    await EjercicioService.delete_ejercicio(ejercicio_id)
    return {"mensaje": "Ejercicio eliminado correctamente"}

@router.get("/", response_model=list[Ejercicio])
async def list_all():
    return await EjercicioService.list_ejercicios()
