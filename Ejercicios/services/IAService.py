# services/gpt_service.py
import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from schemas.Temas import TemaCreate, NivelEnum
from db.db import temas_collection
import hashlib
from typing import Dict
from bson import ObjectId
from fastapi import HTTPException
from Repositorio.TemaRepositorio import TemaRepository


class GPTService:
    def __init__(self):
        endpoint = "https://models.github.ai/inference"
        model = "openai/gpt-4.1"
        token = os.environ["GITHUB_TOKEN"]
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )
        self.tema_repository = TemaRepository()
        self.model = model

    def _generar_hash_pregunta(self, pregunta: Dict) -> str:
        """Genera hash único para una pregunta"""
        contenido = f"{pregunta['pregunta']}_{pregunta['respuesta_correcta']}"
        return hashlib.md5(contenido.encode()).hexdigest()


    async def _filtrar_ejercicios_duplicados(self, tema_nombre: str, nuevos_ejercicios: Dict) -> Dict:
        """
        Filtra ejercicios que ya existen en la base de datos para el tema dado
        
        Args:
            tema_nombre: Nombre del tema a verificar
            nuevos_ejercicios: Ejercicios generados por el LLM (formato {'facil': [...], ...})
            
        Returns:
            Dict: Ejercicios filtrados sin duplicados
        """
        tema_existente = await temas_collection.find_one(
            {"nombre": {"$regex": f"^{tema_nombre}$", "$options": "i"}},
            {"niveles.preguntas": 1}
        )
        
        if not tema_existente:
            return nuevos_ejercicios

        hashes_existentes = set()
        for nivel in tema_existente.get("niveles", []):
            for pregunta in nivel.get("preguntas", []):
                hash_pregunta = self._generar_hash_pregunta(pregunta)
                hashes_existentes.add(hash_pregunta)

        ejercicios_filtrados = {"facil": [], "medio": [], "dificil": []}
        
        for nivel, preguntas in nuevos_ejercicios.items():
            for pregunta in preguntas:
                hash_nuevo = self._generar_hash_pregunta(pregunta)
                if hash_nuevo not in hashes_existentes:
                    ejercicios_filtrados[nivel].append(pregunta)                    
                    hashes_existentes.add(hash_nuevo)  

        return ejercicios_filtrados

    async def generar_ejercicios(self, tema: str, forzar_generacion: bool = False) -> dict:
        """
        Genera ejercicios para un tema, verificando primero si no existe
        
        Args:
            tema: Nombre del tema a generar
            forzar_generacion: Si True, genera ejercicios aunque el tema exista
        
        Returns:
            dict: Resultado de la generación
            
        Raises:
            HTTPException: Si el tema ya existe y no se fuerza la generación
        """
        if not forzar_generacion and await self.tema_repository._verificar_tema_existente(tema):
            raise HTTPException(
                status_code=400,
                detail=f"El tema '{tema}' ya existe en la base de datos. Use forzar_generacion=True para regenerar."
            )

        PROMPT_TEMPLATE = """
            Genera 10 ejercicios de matemáticas para 2° de secundaria (Perú) sobre el tema: {tema}.

            Requisitos:
            1. Formato JSON con 3 niveles de dificultad:
            - 3 ejercicios fáciles (operaciones básicas)
            - 4 ejercicios medios (aplicación de conceptos)
            - 3 ejercicios difíciles (problemas contextualizados)

            2. Estructura cada ejercicio con:
            - pregunta: string claro
            - respuesta_correcta: string o número
            - es_multiple_choice: boolean
            - opciones: array de strings (si es multiple choice)

            3. Contexto peruano (ej. usar soles, referencias locales)

            Ejemplo de formato esperado:
            {{
            "facil": [
                {{
                "pregunta": "¿Cuánto es 2 + 3?",
                "respuesta_correcta": "5",
                "es_multiple_choice": true,
                "opciones": ["3", "4", "5", "6"]
                }}
            ],
            "medio": [...],
            "dificil": [...]
            }}

            TEMA: {tema}
            """
        
        prompt = PROMPT_TEMPLATE.format(tema=tema)
        
        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un experto en educación matemática que genera ejercicios pedagógicos."),
                    UserMessage(prompt),
                ],
                temperature=1.0,
                top_p=1.0,
                model=self.model
            )
            resultado = json.loads(response.choices[0].message.content)
            
            resultado_filtrado = await self._filtrar_ejercicios_duplicados(tema, resultado)
            
            total_ejercicios = sum(len(p) for p in resultado_filtrado.values())
            if total_ejercicios == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Todos los ejercicios generados ya existen en la base de datos"
                )

        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar respuesta del LLM: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar ejercicios con el LLM: {str(e)}"
            )

        niveles = []
        for nivel_str in ["facil", "medio", "dificil"]:
            preguntas = resultado_filtrado.get(nivel_str, [])
            niveles.append({
                "nivel": NivelEnum(nivel_str),
                "preguntas": preguntas
            })

        tema_dict = {
            "nombre": tema,
            "descripcion": f"Ejercicios de {tema} generados por GPT",
            "niveles": niveles
        }

        tema_obj = TemaCreate(**tema_dict)
        
        tema_existente = await temas_collection.find_one({"nombre": tema})
        if tema_existente:
            await temas_collection.update_one(
                {"_id": ObjectId(tema_existente["_id"])},
                {"$set": tema_obj.dict(by_alias=True)}
            )
            operation = "actualizado"
        else:
            await temas_collection.insert_one(tema_obj.dict(by_alias=True))
            operation = "creado"

        return {
            "status": f"Tema {operation} exitosamente",
            "tema": tema,
            "ejercicios_nuevos": resultado_filtrado,
            "ejercicios_generados": sum(len(nivel["preguntas"]) for nivel in niveles),
            "detalle": {
                "facil": len(resultado_filtrado.get("facil", [])),
                "medio": len(resultado_filtrado.get("medio", [])),
                "dificil": len(resultado_filtrado.get("dificil", []))
            }
        }

   
        """
        Analiza patrones de errores en las respuestas del alumno
        
        Args:
            respuestas_alumno: Lista de respuestas del alumno
        
        Returns:
            Dict: Análisis de patrones y recomendaciones
        """
        
        errores = [r for r in respuestas_alumno if not r.get("correcto", True)]
        
        if not errores:
            return {
                "patrones_identificados": [],
                "recomendaciones": "El alumno muestra un excelente desempeño sin errores significativos.",
                "areas_fortaleza": ["Resolución precisa", "Comprensión conceptual sólida"]
            }

        PROMPT_ANALISIS = f"""
        Analiza los patrones de errores en las respuestas de un alumno de matemáticas.
        
        **RESPUESTAS INCORRECTAS:**
        {json.dumps(errores, indent=2)}
        
        **ANÁLISIS REQUERIDO:**
        Identifica patrones comunes en los errores y proporciona recomendaciones pedagógicas.
        
        **FORMATO JSON:**
        {{
            "patrones_identificados": [
                {{
                    "patron": "Descripción del patrón de error",
                    "frecuencia": "alta/media/baja",
                    "concepto_afectado": "Concepto matemático involucrado",
                    "ejemplos": ["ejemplo1", "ejemplo2"]
                }}
            ],
            "recomendaciones": "Recomendaciones específicas para mejorar",
            "estrategias_enseñanza": [
                "Estrategia 1 específica",
                "Estrategia 2 específica"
            ],
            "ejercicios_sugeridos": [
                "Tipo de ejercicio 1",
                "Tipo de ejercicio 2"
            ],
            "areas_fortaleza": ["Fortaleza 1", "Fortaleza 2"]
        }}
        """

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un especialista en análisis pedagógico que identifica patrones de aprendizaje."),
                    UserMessage(PROMPT_ANALISIS),
                ],
                temperature=0.3,
                top_p=0.9,
                model=self.model
            )
            
            analisis = json.loads(response.choices[0].message.content)
            return analisis
            
        except Exception as e:
            return {
                "patrones_identificados": [],
                "recomendaciones": "No se pudo completar el análisis automático. Se recomienda revisión manual.",
                "error": str(e)
            }