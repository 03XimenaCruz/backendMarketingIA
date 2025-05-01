from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import data, visualizations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api/data")
app.include_router(visualizations.router, prefix="/api/visualizations")

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de MarketingIA"}