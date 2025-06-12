from sqlalchemy import Boolean, Column, Integer, String
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
    user_id = Column(Integer, nullable=False) # On liera à un utilisateur plus tard
    service_name = Column(String, unique=True, index=True, nullable=False)
    # On stocke les données chiffrées sous forme binaire
    encrypted_config_data = Column(LargeBinary, nullable=False)