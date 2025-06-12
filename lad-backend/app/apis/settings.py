from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import json

# --- On importe notre nouveau schéma ---
from .. import schemas, models, crud
from .auth import get_current_user, get_db
from ..config import ENCRYPTION_KEY

router = APIRouter()
fernet = Fernet(ENCRYPTION_KEY)

@router.post("/settings/{service_name}", status_code=204)
def save_settings(
    service_name: str, 
    # --- On utilise le nouveau schéma générique ---
    settings_data: schemas.SettingData, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Le reste de la fonction ne change pas, elle est déjà générique !
    config_str = settings_data.model_dump_json()
    encrypted_data = fernet.encrypt(config_str.encode())
    
    crud.save_service_settings(
        db=db, 
        user_id=current_user.id, 
        service_name=service_name, 
        encrypted_data=encrypted_data
    )
    return

@router.get("/settings/{service_name}", response_model=schemas.SettingData)
def get_settings(
    service_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_setting = crud.get_service_settings(db, user_id=current_user.id, service_name=service_name)
    if not db_setting:
        raise HTTPException(status_code=404, detail=f"Settings for {service_name} not found.")
    
    decrypted_data_bytes = fernet.decrypt(db_setting.encrypted_config_data)
    decrypted_data_json = json.loads(decrypted_data_bytes.decode())
    
    return schemas.SettingData(**decrypted_data_json)