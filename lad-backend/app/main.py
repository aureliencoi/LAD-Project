import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import engine
from . import models
from .apis import auth, media, settings, assets, templates # <-- 1. Importer 'templates'

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="LAD - Libraries Assets Designer")

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(media.router, prefix="/api", tags=["Media"])
app.include_router(settings.router, prefix="/api", tags=["Settings"])
app.include_router(assets.router, prefix="/api", tags=["Assets"])
app.include_router(templates.router, prefix="/api", tags=["Templates"]) # <-- 2. Inclure le routeur

BADGES_DATA_DIR = "/data/badges"
os.makedirs(BADGES_DATA_DIR, exist_ok=True)
app.mount("/badges", StaticFiles(directory=BADGES_DATA_DIR), name="user_badges")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue sur l'API de LAD !"}
