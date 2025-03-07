from sqlalchemy.orm import Session
from modelos.modelos import CadenaHotelera, Hotel, TipoHabitacion, Habitacion, Reservacion, TarifaTemporada, Temporada, SessionLocal
from datetime import date

def seed_data():
    """
    Poblar la base de datos con datos de prueba.
    """
    db: Session = SessionLocal()
    
    try:
        # 1. Crear una cadena hotelera
        cadena = CadenaHotelera(nombre="Luxury Hotels")
        db.add(cadena)
        db.commit()
        db.refresh(cadena)
        
        # 2. Crear hoteles asociados a la cadena
        hotel1 = Hotel(sede="Hotel Central", direccion="Av. Principal 123", cupo_maximo=100, cadena_id=cadena.id)
        hotel2 = Hotel(sede="Hotel Playa", direccion="Calle Marítima 456", cupo_maximo=80, cadena_id=cadena.id)
        db.add_all([hotel1, hotel2])
        db.commit()
        db.refresh(hotel1)
        db.refresh(hotel2)
        
        # 3. Crear tipos de habitaciones
        tipo_suite = TipoHabitacion(nombre="Suite")
        tipo_estandar = TipoHabitacion(nombre="Estándar")
        db.add_all([tipo_suite, tipo_estandar])
        db.commit()
        db.refresh(tipo_suite)
        db.refresh(tipo_estandar)
        
        # 4. Crear habitaciones dentro de los hoteles
        habitacion1 = Habitacion(numero="101", tipo_id=tipo_suite.id, precio=200, hotel_id=hotel1.id)
        habitacion2 = Habitacion(numero="102", tipo_id=tipo_estandar.id, precio=100, hotel_id=hotel1.id)
        habitacion3 = Habitacion(numero="201", tipo_id=tipo_suite.id, precio=250, hotel_id=hotel2.id)
        db.add_all([habitacion1, habitacion2, habitacion3])
        db.commit()
        db.refresh(habitacion1)
        db.refresh(habitacion2)
        db.refresh(habitacion3)
        
        # 5. Crear tarifas por temporada para cada tipo de habitación
        tarifa_alta_suite = TarifaTemporada(hotel_id=hotel1.id, tipo_habitacion_id=tipo_suite.id, temporada=Temporada.ALTA, precio=300)
        tarifa_baja_suite = TarifaTemporada(hotel_id=hotel1.id, tipo_habitacion_id=tipo_suite.id, temporada=Temporada.BAJA, precio=180)
        tarifa_alta_estandar = TarifaTemporada(hotel_id=hotel1.id, tipo_habitacion_id=tipo_estandar.id, temporada=Temporada.ALTA, precio=150)
        tarifa_baja_estandar = TarifaTemporada(hotel_id=hotel1.id, tipo_habitacion_id=tipo_estandar.id, temporada=Temporada.BAJA, precio=90)
        db.add_all([tarifa_alta_suite, tarifa_baja_suite, tarifa_alta_estandar, tarifa_baja_estandar])
        db.commit()
        
        # 6. Crear reservaciones en las habitaciones
        reservacion1 = Reservacion(habitacion_id=habitacion1.id, fecha_inicio=date(2024, 7, 10), fecha_fin=date(2024, 7, 15))
        reservacion2 = Reservacion(habitacion_id=habitacion3.id, fecha_inicio=date(2024, 8, 1), fecha_fin=date(2024, 8, 5))
        db.add_all([reservacion1, reservacion2])
        db.commit()
        
        print("Datos de prueba insertados correctamente.")
    
    except Exception as e:
        db.rollback()
        print(f"Error al insertar datos: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
