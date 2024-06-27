from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Configurar la base de datos
engine = create_engine('sqlite:///History.db')
Base = declarative_base()

# Definir el modelo para TiposDeDocumentos
class TiposDeDocumentos(Base):
    __tablename__ = 'TiposDeDocumentos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_de_tipo = Column(String, nullable=False)
    
class CondicionFrenteIva(Base):
    __tablename__ = 'CondicionFrenteIva'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_de_condicion = Column(String, nullable=False)

# Definir el modelo para Facturas
class Facturas(Base):
    __tablename__ = 'Facturas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(String, nullable=False)
    tipo_de_documento_id = Column(Integer, ForeignKey('TiposDeDocumentos.id'), nullable=False)
    condicion_iva = Column(Integer, ForeignKey('CondicionFrenteIva.id'), nullable=False)
    productos = Column(String, nullable=False)  # Almacenar los productos como una cadena
    valor_total = Column(Float(2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    tipo_de_documento = relationship("TiposDeDocumentos")

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Insertar datos en TiposDeDocumentos
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
    CondicionFrenteIva(nombre_de_condicion='Iva Sujeto Excento'),
]

session.add_all(condicion_iva)
session.commit()

# Cerrar la sesión
session.close()

print("Base de datos inicializada con exito.")
