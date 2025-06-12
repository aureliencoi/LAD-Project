from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

def get_user_by_username(db: Session, username: str):
    """Récupère un utilisateur par son nom d'utilisateur."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Crée un nouvel utilisateur dans la base de données."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_service_settings(db: Session, user_id: int, service_name: str):
    return db.query(models.Setting).filter(
        models.Setting.user_id == user_id, 
        models.Setting.service_name == service_name
    ).first()

def save_service_settings(db: Session, user_id: int, service_name: str, encrypted_data: bytes):
    db_setting = get_service_settings(db, user_id, service_name)
    if db_setting:
        # Si les paramètres existent, on les met à jour
        db_setting.encrypted_config_data = encrypted_data
    else:
        # Sinon, on les crée
        db_setting = models.Setting(
            user_id=user_id, 
            service_name=service_name, 
            encrypted_config_data=encrypted_data
        )
        db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting