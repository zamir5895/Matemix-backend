from db.db import ejercicios_collection
from models.Ejerccicio import EjercicioCreate
from bson import ObjectId

class EjercicioRepository:
    def __init__(self):
        pass
    def fix_objectid(self,doc):
        if not doc:
            return doc
        doc = dict(doc)
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def createEjercicio(self, ejercicio: EjercicioCreate):
        try:
            ejercicio_dict = ejercicio.dict()
            result = await ejercicios_collection.insert_one(ejercicio_dict)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error al crear el ejercicio: {e}")
            return None

    async def getEjercicioById(self, id: str):
        try:
            ejercicio = await ejercicios_collection.find_one({"_id": ObjectId(id)})
            print("Ejercicio encontrado:", ejercicio)
            return self.fix_objectid(ejercicio)
        except Exception as e:
            print(f"Error al obtener el ejercicio: {e}")
            return None
    
    
