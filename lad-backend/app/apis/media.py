# lad-backend/app/apis/media.py

import json
import requests # <-- NOUVEL IMPORT
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from pyarr import RadarrAPI, SonarrAPI

# On n'a plus besoin de tmdbv3api ici
# from tmdbv3api import TMDb, Movie as TMDbMovie 

from .. import crud, models
from ..config import ENCRYPTION_KEY
from .auth import get_current_user, get_db

router = APIRouter()

def _get_decrypted_settings(db: Session, user_id: int, service_name: str):
    db_settings = crud.get_service_settings(db, user_id=user_id, service_name=service_name)
    if not db_settings:
        return None
    try:
        fernet = Fernet(ENCRYPTION_KEY)
        decrypted_data_bytes = fernet.decrypt(db_settings.encrypted_config_data)
        return json.loads(decrypted_data_bytes.decode())
    except Exception:
        return None

# --- Les routes /movies et /series ne changent pas ---
@router.get("/movies")
def get_movies(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    radarr_settings = _get_decrypted_settings(db, current_user.id, "radarr")
    if not radarr_settings or not radarr_settings.get('url') or not radarr_settings.get('api_key'):
        return []
    try:
        radarr = RadarrAPI(radarr_settings['url'], radarr_settings['api_key'])
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
        print(f"Erreur de communication avec Radarr: {e}")
        return []

@router.get("/series")
def get_series(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sonarr_settings = _get_decrypted_settings(db, current_user.id, "sonarr")
    if not sonarr_settings or not sonarr_settings.get('url') or not sonarr_settings.get('api_key'):
        return []
    try:
        sonarr = SonarrAPI(sonarr_settings['url'], sonarr_settings['api_key'])
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
        print(f"Erreur de communication avec Sonarr: {e}")
        return []

# --- ROUTE DE DÉTAIL ENTIÈREMENT REVUE AVEC UN APPEL HTTP DIRECT ---
@router.get("/movie/{movie_id}")
def get_movie_detail(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("\n--- [DIRECT API DEBUG] Démarrage de la récupération des détails ---")
    radarr_settings = _get_decrypted_settings(db, current_user.id, "radarr")
    tmdb_settings = _get_decrypted_settings(db, current_user.id, "tmdb")

    if not radarr_settings:
        raise HTTPException(status_code=404, detail="Paramètres Radarr non configurés.")
    if not tmdb_settings or not tmdb_settings.get('api_key'):
        raise HTTPException(status_code=404, detail="Clé API TMDB non configurée.")

    try:
        radarr = RadarrAPI(radarr_settings['url'], radarr_settings['api_key'])
        movie_detail_radarr = radarr.get_movie(movie_id)
        if not movie_detail_radarr:
            raise HTTPException(status_code=404, detail="Film non trouvé dans Radarr.")
        
        tmdb_id = movie_detail_radarr.get('tmdbId')
        tmdb_api_key = tmdb_settings.get('api_key')

        if tmdb_id:
            # On construit l'URL de l'API TMDB manuellement
            tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}&append_to_response=images"
            print(f"--- [DIRECT API DEBUG] Appel à l'URL : {tmdb_url}")
            
            # On fait l'appel direct
            response = requests.get(tmdb_url)
            response.raise_for_status()  # Lève une erreur si le statut n'est pas 200 OK
            
            tmdb_data = response.json()
            
            # --- ESPION : On affiche la réponse brute ---
            print("--- [DIRECT API DEBUG] Réponse JSON brute de TMDB reçue :")
            print(json.dumps(tmdb_data, indent=2)) # Affiche le JSON de manière lisible
            
            # On combine les données de Radarr avec celles de TMDB
            # Le frontend attend les clés 'tmdb_details' et 'tmdb_images'
            movie_detail_radarr['tmdb_details'] = tmdb_data
            # On récupère les images de la réponse
            movie_detail_radarr['tmdb_images'] = tmdb_data.get('images', {})
        
        return movie_detail_radarr
    except requests.exceptions.HTTPError as http_err:
        print(f"--- [DIRECT API DEBUG] ERREUR HTTP : {http_err} - Réponse: {http_err.response.text}")
        raise HTTPException(status_code=500, detail=f"Erreur HTTP de TMDB: {http_err.response.text}")
    except Exception as e:
        print(f"--- [DIRECT API DEBUG] ERREUR CRITIQUE : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de communication avec les services externes: {e}")

# --- La route /series/{id} ne change pas ---
@router.get("/series/{series_id}")
def get_series_detail(series_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # ... (code existant)
    sonarr_settings = _get_decrypted_settings(db, current_user.id, "sonarr")
    if not sonarr_settings:
        raise HTTPException(status_code=404, detail="Paramètres Sonarr non configurés.")
    try:
        sonarr = SonarrAPI(sonarr_settings['url'], sonarr_settings['api_key'])
        series_detail = sonarr.get_series(series_id)
        if not series_detail:
            raise HTTPException(status_code=404, detail="Série non trouvée dans Sonarr.")
        return series_detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de communication avec Sonarr: {e}")
