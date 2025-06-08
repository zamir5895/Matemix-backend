from fastapi import APIRouter, HTTPException
from services.TemaService import TemaService
from models.Temas import CreateTema
from schemas.Temas import Tema

class CrudTemas:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.create_tema, methods=["POST"], response_model=Tema)
        self.router.add_api_route(
            "/{salon_id}",  
            self.get_temas_by_salon_id,
            methods=["GET"],
            response_model=list[Tema]
        )
        self.router.add_api_route(
            "/topic/temas/{tema_id}",
            self.get_tema_by_tema_id,
            methods=["GET"],
            response_model=Tema
        )
        self.service = TemaService()
    
    async def create_tema(self, tema: CreateTema):
        try:
            result = await self.service.createTema(tema)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result["tema"]
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_temas_by_salon_id(self, salon_id: int):
        try:
            temas = await self.service.getTemasBySalonId(salon_id)
            if "error" in temas:
                raise HTTPException(status_code=400, detail=temas["error"])
            return temas
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_tema_by_tema_id(self, tema_id: str):
        try:
            tema = await self.service.getTemaByTemaId(tema_id)
            if "error" in tema:
                raise HTTPException(status_code=404, detail=tema["error"])
            return tema
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))    

crud_temas = CrudTemas()
router = crud_temas.router