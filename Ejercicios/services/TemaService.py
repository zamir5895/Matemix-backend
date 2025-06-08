from Repositorio.TemaRepositorio import TemaRepository
from models.Temas import CreateTema
from schemas.Temas import Tema
class TemaService:
    def __init__(self):
        self.tema_repository = TemaRepository()
    async def createTema(self, createTema: CreateTema):
        
        try:
            print(createTema)
            if await self.tema_repository.exists(createTema.nombre, createTema.classroom_id):

                return {"error": "El tema ya existe en el salon"}
            print("Paso el error")
            created_tema = await self.tema_repository.createTema(createTema)
            if created_tema is None:
                return {"error": "No se pudo crear el tema"}
            tema = await self.tema_repository.getTemaById(created_tema)
            tema["_id"]=str(tema["_id"])  
            tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]  # Convertir ObjectId a str
            print(tema)

            return {"tema": Tema(**tema)}
        except Exception as e:
            return {"error": str(e)}
    
    async def getTemasBySalonId(self, classroom_id: int):
        try:
            temas = await self.tema_repository.getTemasBySalonId(classroom_id)
            for tema in temas:
                tema["_id"] = str(tema["_id"]) 
                tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]  # Convertir ObjectId a str
            return temas
        except Exception as e:
            return {"error": str(e)}
    
    async def getTemaByTemaId(self, tema_id: str):
        try:
            tema = await self.tema_repository.getTemaById(tema_id)
            if tema is None:
                return {"error": "Tema no encontrado"}
            tema["_id"] = str(tema["_id"])
            tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]  # Convertir ObjectId a str
            return Tema(**tema)
        except Exception as e:
            return {"error": str(e)}