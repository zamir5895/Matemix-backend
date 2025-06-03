from db.db import temas_collection
from schemas.Temas import TemaCreate

from bson import ObjectId

class TemaRepository:
    async def exists(nombre: str, curso_id: int):
        existing_tema = await temas_collection.find_one({"nombre": nombre, "curso_id": curso_id})
        return existing_tema is not None

    async def _verificar_tema_existente(self, tema: str) -> bool:
        """Verifica si un tema ya existe en la base de datos"""
        tema_existente = await temas_collection.find_one(
            {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
        )
        return tema_existente is not None
    
    """ Buscamos el tema si existe por el classroom_id"""

    async def existsByClassroom_id(self, classroom_id: int) -> bool:
        """
        Verifica si un tema ya existe en la base de datos por su classroom_id.
        
        Args:
            classroom_id (str): El ID del classroom del tema a verificar.
        
        Returns:
            bool: True si el tema existe, False en caso contrario.
        """
        tema_existente = await temas_collection.find_one({"classroom_id": classroom_id})
        return tema_existente is not None
    
    """Obtenemos los temas por el classroom_id"""
    async def getTemasBySalonId(self, classroom_id:int):
        """
        Obtiene todos los temas asociados a un classroom_id.
        
        Args:
            classroom_id (int): El ID del classroom del que se desean obtener los temas.
        
        Returns:
            List[Dict]: Lista de temas asociados al classroom_id.
        """
        temas = await temas_collection.find({"classroom_id": classroom_id}).to_list(length=None)
        return temas