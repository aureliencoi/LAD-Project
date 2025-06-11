import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Le chemin du dossier de données persistantes à l'intérieur du conteneur Docker
# Nous l'utilisons déjà pour être prêts pour le déploiement
DATA_DIR = "data"
# En développement local, cela créera un dossier 'data' dans 'lad-backend'
os.makedirs(DATA_DIR, exist_ok=True) 

# URL de connexion pour la base de données SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'lad.db')}"

# Moteur de la base de données
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # Requis pour SQLite pour autoriser l'utilisation dans plusieurs threads
    connect_args={"check_same_thread": False} 
)

# Session pour les transactions avec la BDD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour nos modèles de BDD (ex: User)
Base = declarative_base()