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