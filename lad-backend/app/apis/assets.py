# lad-backend/app/apis/assets.py

import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel # <-- 1. Importer BaseModel
from typing import List

from ..models import User
from .auth import get_current_user

router = APIRouter()

# Le chemin de base où les badges seront stockés de manière persistante
BADGES_DIR = "/data/badges"

# --- CORRECTION : La classe Badge doit hériter de BaseModel ---
class Badge(BaseModel):
    name: str
    path: str

@router.post("/badges", response_model=Badge)
async def upload_badge(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user)
):
    """
    Reçoit un fichier image et le sauvegarde dans un dossier
    spécifique à l'utilisateur.
    """
    # Crée un dossier pour l'utilisateur s'il n'existe pas
    user_badge_dir = os.path.join(BADGES_DIR, str(current_user.id))
    os.makedirs(user_badge_dir, exist_ok=True)
    
    file_path = os.path.join(user_badge_dir, file.filename)

    # Vérifie si un fichier avec le même nom existe déjà pour éviter les doublons
    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail="Un badge avec ce nom existe déjà.")

    # Copie le contenu du fichier uploadé dans le dossier de destination
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # On renvoie le chemin relatif pour que le frontend puisse l'utiliser
    return {"name": os.path.splitext(file.filename)[0], "path": f"/badges/{current_user.id}/{file.filename}"}

@router.get("/badges", response_model=List[Badge])
def get_custom_badges(current_user: User = Depends(get_current_user)):
    """
    Renvoie la liste des badges personnalisés pour l'utilisateur connecté.
    """
    user_badge_dir = os.path.join(BADGES_DIR, str(current_user.id))
    
    # Si l'utilisateur n'a pas encore de dossier de badges, on renvoie une liste vide
    if not os.path.isdir(user_badge_dir):
        return []

    badges = []
    for filename in os.listdir(user_badge_dir):
        # On s'assure de ne lister que les fichiers (pas les sous-dossiers)
        if os.path.isfile(os.path.join(user_badge_dir, filename)):
            badges.append({
                "name": os.path.splitext(filename)[0], # Nom du badge (sans l'extension)
                "path": f"/badges/{current_user.id}/{filename}" # Chemin d'accès web
            })
    return badges
