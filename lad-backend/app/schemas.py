from pydantic import BaseModel, EmailStr

# Schéma pour la création d'un utilisateur (données reçues par l'API)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schéma de base pour un utilisateur (sans le mot de passe)
class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        # Permet à Pydantic de lire les données depuis des modèles SQLAlchemy
        from_attributes = True

# Schéma pour le jeton d'accès
class Token(BaseModel):
    access_token: str
    token_type: str

# Schéma pour les données contenues dans le jeton
class TokenData(BaseModel):
    username: str | None = None

class RadarrSettings(BaseModel):
    url: str
    api_key: str