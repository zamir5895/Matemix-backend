from motor.motor_asyncio import AsyncIOMotorClient
from db.config import settings

client = None
database = None

temas_collection = None
examenes_subtopicos = None
examenes_topicos = None
exam = None
pdf_resource = None
ejercicios_resueltos = None

async def connect_to_mongo():
    global client, database
    global temas_collection, examenes_subtopicos, examenes_topicos, exam, pdf_resource, ejercicios_resueltos
    client = AsyncIOMotorClient(settings.mongo_uri)
    database = client[settings.database_name]
    temas_collection = database.get_collection("temas")
    examenes_subtopicos = database.get_collection("examenes_subtopicos")
    examenes_topicos = database.get_collection("examenes_topicos")
    exam = database.get_collection("exam")
    pdf_resource = database.get_collection("pdf_resource")
    ejercicios_resueltos = database.get_collection("ejercicios_resueltos")

async def close_mongo_connection():
    global client
    if client:
        client.close()