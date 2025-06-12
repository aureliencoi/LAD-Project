# lad-backend/app/apis/media.py

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from pyarr import RadarrAPI, SonarrAPI

# --- NOUVEAUX IMPORTS ---
from tmdbv3api import TMDb, Movie as TMDbMovie

from .. import crud, models
from ..config import ENCRYPTION_KEY, TMDB_API_KEY # <-- Importer la clé TMDB
from .auth import get_current_user, get_db

# --- CONFIGURATION TMDB ---
tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = 'fr-FR'

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

@router.get("/movie/{movie_id}")
def get_movie_detail(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        settings = _get_decrypted_settings(db, current_user.id, "radarr")
        radarr = RadarrAPI(settings['url'], settings['api_key'])
        movie_detail_radarr = radarr.get_movie(movie_id)
        if not movie_detail_radarr:
            raise HTTPException(status_code=404, detail="Film non trouvé dans Radarr.")
        
        # --- NOUVELLE LOGIQUE TMDB ---
        # On récupère l'ID TMDB depuis les données de Radarr
        tmdb_id = movie_detail_radarr.get('tmdbId')
        if tmdb_id:
            tmdb_movie_api = TMDbMovie()
            # On récupère les images pour ce film
            images = tmdb_movie_api.images(tmdb_id)
            # On ajoute les images à notre objet de réponse
            # On peut ajouter d'autres infos si on veut (acteurs, etc.)
            movie_detail_radarr['tmdb_posters'] = images.get('posters', [])
            movie_detail_radarr['tmdb_backdrops'] = images.get('backdrops', [])
        
        return movie_detail_radarr
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de communication avec les services externes: {e}")

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