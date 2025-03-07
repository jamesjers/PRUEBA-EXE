from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.orm import Session
from modelos.modelos import Hotel, TipoHabitacion, SessionLocal
from fastapi.staticfiles import StaticFiles
from reactpy.backend.fastapi import configure
from interfaz.vistas import App, SimpleApp
from datetime import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Reservas Hoteleras")


app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/disponibilidad/")
def verificar_disponibilidad(fecha: str, db: Session = Depends(get_db)):
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    
    habitaciones_reservadas = db.query(Habitacion.id).join(
        Reservacion, Habitacion.id == Reservacion.habitacion_id
    ).filter(
        Reservacion.fecha_inicio <= fecha_obj,
        Reservacion.fecha_fin >= fecha_obj
    ).distinct().subquery()
    
    hoteles_con_disponibilidad = db.query(Hotel).join(
        Habitacion, Hotel.id == Habitacion.hotel_id
    ).filter(
        ~Habitacion.id.in_(habitaciones_reservadas)
    ).distinct().all()
    
    return {"hoteles_disponibles": [hotel.nombre for hotel in hoteles_con_disponibilidad]}

@app.get("/api/tarifas/")
def obtener_tarifas(sitio_id: int, temporada: str, personas: int, tipo_alojamiento: str, db: Session = Depends(get_db)):
    tarifa = db.query(TipoHabitacion).filter(
        TipoHabitacion.hotel_id == sitio_id,
        TipoHabitacion.tipo == tipo_alojamiento,
        TipoHabitacion.temporada == temporada
    ).first()
    
    if tarifa:
        return {"tarifa": tarifa.precio * personas}
    return {"error": "No se encontró tarifa"}


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


configure(app, App)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",
        proxy_headers=True  
    )