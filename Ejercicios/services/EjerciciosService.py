from Repositorio.EjercicioRepositorio import EjercicioRepository
from schemas.Temas import Ejercicio, EjercicioCreate

class EjercicioService:
    @staticmethod
    async def create_ejercicio(ejercicio: EjercicioCreate):
        return await EjercicioRepository.create(ejercicio)

    @staticmethod
    async def get_ejercicio_by_id(ejercicio_id: str):
        doc = await EjercicioRepository.get_by_id(ejercicio_id)
        if doc:
            return Ejercicio(**doc)
        return None

    @staticmethod
    async def update_ejercicio(ejercicio_id: str, ejercicio: EjercicioCreate):
        await EjercicioRepository.update(ejercicio_id, ejercicio)

    @staticmethod
    async def delete_ejercicio(ejercicio_id: str):
        await EjercicioRepository.delete(ejercicio_id)

    @staticmethod
    async def list_ejercicios():
        ejercicios = []
        async for doc in EjercicioRepository.list_all():
            ejercicios.append(Ejercicio(**doc))
        return ejercicios