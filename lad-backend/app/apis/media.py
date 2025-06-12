# lad-backend/app/apis/media.py

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from pyarr import RadarrAPI, SonarrAPI

from .. import crud, models
from ..config import ENCRYPTION_KEY
from .auth import get_current_user, get_db

router = APIRouter()

# --- HELPER FUNCTION TO GET SETTINGS ---
# Pour éviter la répétition de code, on crée une fonction réutilisable
def _get_decrypted_settings(db: Session, user_id: int, service_name: str):
    db_settings = crud.get_service_settings(db, user_id=user_id, service_name=service_name)
    if not db_settings:
        raise HTTPException(
            status_code=404, 
            detail=f"Les paramètres pour {service_name} ne sont pas configurés."
        )
    try:
        fernet = Fernet(ENCRYPTION_KEY)
        decrypted_data_bytes = fernet.decrypt(db_settings.encrypted_config_data)
        return json.loads(decrypted_data_bytes.decode())
    except Exception:
        raise HTTPException(status_code=500, detail=f"Impossible de déchiffrer les paramètres {service_name}.")

# --- ROUTES EXISTANTES (MODIFIÉES POUR UTILISER LA FONCTION HELPER) ---

@router.get("/movies")
def get_movies(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        settings = _get_decrypted_settings(db, current_user.id, "radarr")
        radarr = RadarrAPI(settings['url'], settings['api_key'])
        radarr_movies = radarr.get_movie()
        
        formatted_movies = []
        for movie in radarr_movies:
            poster_url = ""
            if movie.get('images'):
                for image in movie['images']:
                    if image.get('coverType') == "poster":
                        poster_url = image.get('remoteUrl') or image.get('url')
                        break
            formatted_movies.append({ "id": movie.get('id'), "title": movie.get('title'), "year": movie.get('year'), "poster_url": poster_url })
        return formatted_movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de communication avec Radarr: {e}")

@router.get("/series")
def get_series(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        settings = _get_decrypted_settings(db, current_user.id, "sonarr")
        sonarr = SonarrAPI(settings['url'], settings['api_key'])
        sonarr_series = sonarr.get_series()

        formatted_series = []
        for series in sonarr_series:
            poster_url = ""
            if series.get('images'):
                for image in series['images']:
                    if image.get('coverType') == "poster":
                        poster_url = image.get('remoteUrl') or image.get('url')
                        break
            formatted_series.append({ "id": series.get('id'), "title": series.get('title'), "year": series.get('year'), "poster_url": poster_url })
        return formatted_series
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de communication avec Sonarr: {e}")

# --- NOUVELLES ROUTES POUR LES DÉTAILS ---

@router.get("/movie/{movie_id}")
def get_movie_detail(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        settings = _get_decrypted_settings(db, current_user.id, "radarr")
        radarr = RadarrAPI(settings['url'], settings['api_key'])
        # La bibliothèque Radarr utilise get_movie() pour obtenir un ou tous les films
        # On doit donc filtrer le résultat nous-mêmes.
        movie_detail = radarr.get_movie(movie_id)
        if not movie_detail:
            raise HTTPException(status_code=404, detail="Film non trouvé dans Radarr.")
        # La fonction retourne directement les détails du film, pas besoin de reformater pour l'instant
        return movie_detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de communication avec Radarr: {e}")

@router.get("/series/{series_id}")
def get_series_detail(series_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        settings = _get_decrypted_settings(db, current_user.id, "sonarr")
        sonarr = SonarrAPI(settings['url'], settings['api_key'])
        # La méthode get_series de pyarr avec un id retourne les détails de la série
        series_detail = sonarr.get_series(series_id)
        if not series_detail:
            raise HTTPException(status_code=404, detail="Série non trouvée dans Sonarr.")
        return series_detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de communication avec Sonarr: {e}")