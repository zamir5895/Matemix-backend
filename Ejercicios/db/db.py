from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MOGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MOGO_URI)
database = client.learning_platform

temas_collection = database.get_collection("temas")
examenes_subtopicos = database.get_collection("examenes_subtopicos")
examenes_topicos = database.get_collection("examenes_topicos")
exam= database.get_collection("exam")
pdf_resource = database.get_collection("pdf_resource")
ejercicios_resueltos = database.get_collection("ejercicios_resueltos")  