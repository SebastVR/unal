from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.job import (
    router_job,
)  # Asegúrate de que el nombre del archivo y la importación sean correctos

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origines
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Inclusión de los routers
app.include_router(
    router_job,
    prefix="/jobs",  # Define el prefijo para todas las rutas de jobs
    tags=["jobs"],  # Etiqueta para organizar en la documentación de la API
)
