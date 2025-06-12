from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from .auth import get_current_user, get_db

router = APIRouter()

@router.post("/templates", response_model=schemas.Template, status_code=201)
def create_template(
    template: schemas.TemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Crée un nouveau template pour l'utilisateur connecté.
    """
    return crud.create_user_template(db=db, template=template, user_id=current_user.id)

@router.get("/templates", response_model=List[schemas.Template])
def read_templates(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Récupère tous les templates de l'utilisateur connecté.
    """
    return crud.get_templates_by_user(db=db, user_id=current_user.id)
