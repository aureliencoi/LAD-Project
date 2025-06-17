from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from .. import crud, models, schemas, security
from ..database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()

# Dépendance pour obtenir une session de BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dépendance pour obtenir l'utilisateur actuel à partir d'un token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Enregistre un nouvel utilisateur.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà")
    created_user = crud.create_user(db=db, user=user)
    return created_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Fournit un jeton d'accès après vérification de l'utilisateur.
    """
    print("\n--- [LOGIN DEBUG] Tentative de connexion pour l'utilisateur:", form_data.username)
    user = crud.get_user_by_username(db, username=form_data.username)
    
    if not user:
        print("--- [LOGIN DEBUG] ERREUR: Utilisateur non trouvé dans la BDD.")
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

    print("--- [LOGIN DEBUG] Utilisateur trouvé. Vérification du mot de passe...")
    is_password_correct = security.verify_password(form_data.password, user.hashed_password)
    print(f"--- [LOGIN DEBUG] Le mot de passe est-il correct ? -> {is_password_correct}")

    if not is_password_correct:
        print("--- [LOGIN DEBUG] ERREUR: Le mot de passe est incorrect.")
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print("--- [LOGIN DEBUG] Mot de passe correct. Jeton créé.")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.UserBase)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Route protégée qui renvoie les informations de l'utilisateur connecté.
    """
    return current_user