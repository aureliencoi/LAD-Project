from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Schémas existants (User, Token, SettingData) ---
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

class SettingData(BaseModel):
    url: Optional[str] = None
    api_key: str

# --- NOUVEAUX SCHÉMAS POUR LES TEMPLATES ---

# Schéma pour les données reçues lors de la création d'un template
class TemplateCreate(BaseModel):
    name: str
    template_data: str # Le JSON du canvas sera envoyé comme une chaîne de caractères

# Schéma pour les données renvoyées par l'API (lecture d'un template)
class Template(BaseModel):
    id: int
    name: str
    template_data: str
    owner_id: int

    class Config:
        from_attributes = True
