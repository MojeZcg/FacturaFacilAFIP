from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurar la base de datos
DATABASE_URL = 'sqlite:///History.db'

# Crear una instancia del motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear una clase base para los modelos
Base = declarative_base()

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()