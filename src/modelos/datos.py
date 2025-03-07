from sqlalchemy.orm import Session
from modelos import CadenaHotelera, Hotel, Habitacion, TipoHabitacion, engine, SessionLocal

def seed_data():
    session = SessionLocal()
    try:
        # Verificar si la cadena hotelera ya existe
        cadena = session.query(CadenaHotelera).filter_by(nombre="hoteles_exe").first()
        if not cadena:
            cadena = CadenaHotelera(nombre="hoteles_exe")
            session.add(cadena)
            session.commit()
        
        # Crear tipos de habitación
        tipos_habitacion = {
            "estándar": TipoHabitacion(nombre="estándar"),
            "premium": TipoHabitacion(nombre="premium"),
            "VIP": TipoHabitacion(nombre="VIP")
        }
        session.add_all(tipos_habitacion.values())
        session.commit()
        
        # Definir hoteles y habitaciones
        hoteles_data = [
            {"nombre": "Barranquilla", "habitaciones": [(30, "estándar"), (3, "premium")], "cupo": 4},
            {"nombre": "Cali", "habitaciones": [(20, "premium"), (2, "VIP")], "cupo": 6},
            {"nombre": "Cartagena", "habitaciones": [(10, "estándar"), (1, "premium")], "cupo": 8},
            {"nombre": "Bogotá", "habitaciones": [(20, "estándar"), (20, "premium"), (2, "VIP")], "cupo": 6},
        ]
        
        for hotel_data in hoteles_data:
            hotel = Hotel(sede=hotel_data["nombre"], direccion=f"{hotel_data['nombre']} - Dirección", cadena_id=cadena.id, cupo_maximo=hotel_data["cupo"])
            session.add(hotel)
            session.commit()
            
            # Agregar habitaciones
            for cantidad, tipo in hotel_data["habitaciones"]:
                for i in range(1, cantidad + 1):
                    habitacion = Habitacion(numero=f"{hotel.id}-{i}", tipo_id=tipos_habitacion[tipo].id, precio=100 * (i % 5 + 1), hotel_id=hotel.id)
                    session.add(habitacion)
        
        session.commit()
        print("Datos insertados correctamente")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
