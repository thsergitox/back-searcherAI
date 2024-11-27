from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
app = FastAPI()

app = FastAPI(
    title="LabLab Hackathon", 
    description="Multi Agetn System for Knowledge Graph Construction",
    version="0.1"
)


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)


app.include_router(router, prefix="/api")