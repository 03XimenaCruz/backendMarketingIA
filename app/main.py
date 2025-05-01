from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import data, visualizations

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",           # Desarrollo local
        "https://marketing-ia-ximena.netlify.app/",    # Reemplaza con la URL de tu frontend en Netlify
        # Opcional: usa ["*"] para permitir todos los orígenes (solo para pruebas)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api/data")
app.include_router(visualizations.router, prefix="/api/visualizations")

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de MarketingIA"}