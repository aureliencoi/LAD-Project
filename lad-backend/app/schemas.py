from pydantic import BaseModel, EmailStr
from typing import Optional # Assurez-vous d'avoir cet import

# --- SCHÉMAS UTILISATEUR ET TOKEN (Existants) ---
class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- NOUVEAU SCHÉMA GÉNÉRIQUE POUR LES PARAMÈTRES ---
class SettingData(BaseModel):
    # On rend l'URL optionnelle car TMDB n'en a pas besoin
    url: Optional[str] = None
    # La clé API est toujours requise
    api_key: str