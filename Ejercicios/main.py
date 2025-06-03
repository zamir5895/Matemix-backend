from fastapi import FastAPI
from db.config import settings
from db.db import connect_to_mongo, close_mongo_connection
from crud.EjerciciosCrud import router as ejercicios_router 

app = FastAPI(
    title="Matemix Content Service",
    description="Microservicio para ejercicios y recursos educativos",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Incluye el router aquí
app.include_router(ejercicios_router, prefix="/exercises", tags=["Ejercicios"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Matemix Content Service!"}