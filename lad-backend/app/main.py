import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Assurez-vous que cet import est présent
from fastapi.staticfiles import StaticFiles

from .database import engine
from . import models
from .apis import auth, media, settings, assets, templates

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="LAD - Libraries Assets Designer")

# --- CORRECTION : On s'assure que le middleware CORS est bien là et correct ---
# Liste des origines autorisées à faire des requêtes
origins = [
    "http://localhost:5173", # L'adresse de votre frontend Vue.js
    "http://localhost:4200", # L'adresse de l'ancien frontend Angular (au cas où)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Autorise ces origines
    allow_credentials=True,    # Autorise les cookies/tokens
    allow_methods=["*"],         # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],         # Autorise tous les en-têtes
)
# --- FIN DE LA SECTION CORS ---

# Inclusion des routeurs de l'API
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(media.router, prefix="/api", tags=["Media"])
app.include_router(settings.router, prefix="/api", tags=["Settings"])
app.include_router(assets.router, prefix="/api", tags=["Assets"])
app.include_router(templates.router, prefix="/api", tags=["Templates"])

# Service des fichiers statiques pour les badges
BADGES_DATA_DIR = "/data/badges"
os.makedirs(BADGES_DATA_DIR, exist_ok=True)
app.mount("/badges", StaticFiles(directory=BADGES_DATA_DIR), name="user_badges")

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint racine pour vérifier que l'API est en ligne.
    """
    return {"message": "Bienvenue sur l'API de LAD !"}