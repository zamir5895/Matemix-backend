from fastapi import APIRouter, HTTPException
from services.EjerciciosService import EjercicioService
from schemas.Temas import Ejercicio, EjercicioCreate

class CrudEjercicios:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/generar/{subtema_id}",
            self.create_ejercicio,
            methods=["GET"],
            response_model=dict
        )

        self.router.add_api_route(
            "/{subtema_id}",
            self.get_ejercicios_by_subtema_id,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/{subtema_id}",
            self.getInfoBySubtemaId,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/tema/{tema_id}",
            self.getInfoByTemaId,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/nivel/{subtema_id}/{nivel}",
            self.getEjerciciosBySubtemaIdAndNivel,
            methods=["GET"],
            response_model=dict
        )
        self.service = EjercicioService()

    async def create_ejercicio(self, subtema_id: str):
        try:
            result = await self.service.generar_ejercicios_with_gpt(subtema_id)
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_ejercicios_by_subtema_id(self, subtema_id: str):
        try:
            result = await self.service.getEjerciciosBySubTemaId(subtema_id)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def getInfoBySubtemaId(self, subtema_id: str):
        try:
            response = await self.service.getInfoBySubtemId(subtema_id)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def getInfoByTemaId(self, tema_id: str):
        try:
            response = await self.service.getInfoByTemaId(tema_id)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def getEjerciciosBySubtemaIdAndNivel(self, subtema_id: str, nivel: str):
        try:
            response = await self.service.getEjerciciosByNivel(subtema_id, nivel)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
crud_ejercicios = CrudEjercicios()
router = crud_ejercicios.router
