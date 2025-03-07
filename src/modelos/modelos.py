from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from enum import Enum as PyEnum

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Temporadas
class Temporada(PyEnum):
    ALTA = "alta"
    BAJA = "baja"

# Cadena hotelera
class CadenaHotelera(Base):
    __tablename__ = "cadenas_hoteleras"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    hoteles = relationship("Hotel", back_populates="cadena_hotelera")

# Hoteles
class Hotel(Base):
    __tablename__ = "hoteles"
    id = Column(Integer, primary_key=True, index=True)
    sede = Column(String, index=True)
    direccion = Column(String)
    cupo_maximo = Column(Integer)  
    cadena_id = Column(Integer, ForeignKey("cadenas_hoteleras.id"))
    cadena_hotelera = relationship("CadenaHotelera", back_populates="hoteles")
    habitaciones = relationship("Habitacion", back_populates="hotel")
    tarifas = relationship("TarifaTemporada", back_populates="hotel")

# Tipo de Habitación
class TipoHabitacion(Base):
    __tablename__ = "tipos_habitacion"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    habitaciones = relationship("Habitacion", back_populates="tipo_habitacion")

# Habitaciones
class Habitacion(Base):
    __tablename__ = "habitaciones"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, index=True)
    tipo_id = Column(Integer, ForeignKey("tipos_habitacion.id"))
    precio = Column(Integer)
    hotel_id = Column(Integer, ForeignKey("hoteles.id"))
    hotel = relationship("Hotel", back_populates="habitaciones")
    tipo_habitacion = relationship("TipoHabitacion", back_populates="habitaciones")
    reservaciones = relationship("Reservacion", back_populates="habitacion")

# Reservaciones
class Reservacion(Base):
    __tablename__ = "reservaciones"
    id = Column(Integer, primary_key=True, index=True)
    habitacion_id = Column(Integer, ForeignKey("habitaciones.id"))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    habitacion = relationship("Habitacion", back_populates="reservaciones")

# Tarifas por Temporada
class TarifaTemporada(Base):
    __tablename__ = "tarifas_temporada"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hoteles.id"))
    tipo_habitacion_id = Column(Integer, ForeignKey("tipos_habitacion.id"))
    temporada = Column(Enum(Temporada))
    precio = Column(Integer)
    hotel = relationship("Hotel", back_populates="tarifas")
    tipo_habitacion = relationship("TipoHabitacion")

Base.metadata.create_all(bind=engine)
