from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from .database import Base
from sqlalchemy import LargeBinary

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    service_name = Column(String, unique=True, index=True, nullable=False)
    encrypted_config_data = Column(LargeBinary, nullable=False)

# --- NOUVELLE CLASSE POUR LES TEMPLATES ---
class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    # Le JSON complet du canvas sera stocké ici sous forme de texte
    template_data = Column(Text, nullable=False)
    # Chaque template appartient à un utilisateur
    owner_id = Column(Integer, ForeignKey("users.id"))
