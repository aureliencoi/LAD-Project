from fastapi import FastAPI
from .database import engine
from . import models

# Importez le routeur que nous venons de créer
from .apis import auth

# Crée les tables dans la base de données (pour le développement)
models.Base.metadata.create_all(bind=engine)

# Crée l'instance de l'application FastAPI
app = FastAPI(title="LAD - Libraries Assets Designer")

# Incluez le routeur d'authentification
# Toutes les routes de ce routeur commenceront par /auth
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint racine pour vérifier que l'API est en ligne.
    """
    return {"message": "Bienvenue sur l'API de LAD !"}