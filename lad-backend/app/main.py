from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .apis import auth, media, settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="LAD - Libraries Assets Designer")

# --- AJOUTER CE BLOC DE CODE ---
# Configuration de CORS
origins = [
    "http://localhost:4200", # L'URL de notre frontend Angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- FIN DU BLOC À AJOUTER ---


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(media.router, prefix="/api", tags=["Media"])
app.include_router(settings.router, prefix="/api", tags=["Settings"]) 

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue sur l'API de LAD !"}