"""
Create a database with id_types and condition_iva
"""

from datetime import datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Configurar la base de datos
engine = create_engine('sqlite:///History.db')
Base = declarative_base()

# Definir el modelo para TiposDeDocumentos
class TiposDeDocumentos(Base):
    # pylint: disable=too-few-public-methods
    """
    Clase para representar el modelo de TiposDeDocumentos.
    """
    __tablename__ = 'TiposDeDocumentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_de_tipo = Column(String, nullable=False)

# Definir el modelo para CondicionFrenteIva
class CondicionFrenteIva(Base):
    # pylint: disable=too-few-public-methods
    """
    Clase para representar el modelo de CondicionFrenteIva.
    """
    __tablename__ = 'CondicionFrenteIva'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_de_condicion = Column(String, nullable=False)

# Definir el modelo para Facturas
class Facturas(Base):
    # pylint: disable=too-few-public-methods
    """
    Clase para representar el modelo de Facturas.
    """
    __tablename__ = 'Facturas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(String, nullable=True)
    tipo_de_documento_id = Column(Integer, ForeignKey('TiposDeDocumentos.id'), nullable=False)
    condicion_iva = Column(Integer, ForeignKey('CondicionFrenteIva.id'), nullable=False)
    productos = Column(JSON, nullable=False)
    valor_total = Column(Float(2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    tipo_de_documento = relationship("TiposDeDocumentos")

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def inicializar_base_de_datos():
    """
    Inicializa la base de datos con datos predeterminados.
    """
    tipos_documentos = [
        TiposDeDocumentos(nombre_de_tipo='CUIL'),
        TiposDeDocumentos(nombre_de_tipo='CUIT'),
        TiposDeDocumentos(nombre_de_tipo='DNI'),
    ]

    session.add_all(tipos_documentos)
    session.commit()

    condicion_iva = [
        CondicionFrenteIva(nombre_de_condicion='Consumidor Final'),
        CondicionFrenteIva(nombre_de_condicion='Iva Responsable Inscripto'),
        CondicionFrenteIva(nombre_de_condicion='Iva Sujeto Exento'),
    ]

    session.add_all(condicion_iva)
    session.commit()

    print("Base de datos inicializada con éxito.")

# Inicializar la base de datos (solo una vez, cuando sea necesario)
if __name__ == "__main__":
    inicializar_base_de_datos()
    session.close()
