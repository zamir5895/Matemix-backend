from db.db import subtemas_collection
from schemas.Temas import EjercicioCreate
from bson import ObjectId

class EjercicioRepository:
    @staticmethod
    async def create(ejercicio: EjercicioCreate):
        result = await subtemas_collection.insert_one(ejercicio.dict(by_alias=True))
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(ejercicio_id: str):
        return await subtemas_collection.find_one({"_id": ObjectId(ejercicio_id)})

    @staticmethod
    async def update(ejercicio_id: str, ejercicio: EjercicioCreate):
        await subtemas_collection.update_one(
            {"_id": ObjectId(ejercicio_id)},
            {"$set": ejercicio.dict(by_alias=True)}
        )

    @staticmethod
    async def delete(ejercicio_id: str):
        await subtemas_collection.delete_one({"_id": ObjectId(ejercicio_id)})

    @staticmethod
    async def list_all():
        return subtemas_collection.find()

