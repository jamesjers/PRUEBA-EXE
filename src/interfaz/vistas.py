from reactpy import component, html, use_state, use_effect
from reactpy_router import browser_router, route
import json



# Componente para cargar CSS externo
@component
def Layout(children):
    return html.div(
        html.head(
            html.link({"rel": "stylesheet", "href": "/static/styles.css"})
        ),
        html.div(children)
    )

@component
def PageNotFound():
    return html.div(
        {"class": "container"},
        html.h1("404 - Página no encontrada"),
        html.p("La página que buscas no existe.")
    )

@component
def Bienvenida():
    return html.div(
        {"class": "container"},
        html.h1("Bienvenido al Sistema de Reservas"),
        html.p("Gestiona tus reservas de hotel de manera rápida y sencilla."),
        html.a(
            {
                "href": "/disponibilidad",
                "class": "button-primary nav-link"
            },
            "Entrar"
        )
    )


@component
def Disponibilidad():
    fecha, set_fecha = use_state("")
    hoteles, set_hoteles = use_state([])
    buscando, set_buscando = use_state(False)
    error, set_error = use_state("")
    
    def actualizar_fecha(e):
        set_fecha(e["target"]["value"])
        set_hoteles([])
        set_error("")
    
    def buscar_hoteles(e):
        if not fecha:
            set_error("Por favor selecciona una fecha")
            return
            
        set_buscando(True)
        set_error("")
        
        import httpx
        
        async def fetch_hoteles():
            try:
                response = await httpx.AsyncClient().get(
                    f"/api/disponibilidad/?fecha={fecha}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    set_hoteles(data.get("hoteles_disponibles", []))
                else:
                    set_error(f"Error al consultar disponibilidad: {response.status_code}")
            except Exception as e:
                set_error(f"Error de conexión: {str(e)}")
            finally:
                set_buscando(False)
        
        import asyncio
        asyncio.create_task(fetch_hoteles())
    
    return html.div(
        {"class": "container-green"},
        html.h1("Disponibilidad de Hoteles"),
        html.p("Consulta los hoteles disponibles en la fecha seleccionada."),
        html.div(
            {"style": {"margin": "20px auto", "max-width": "500px"}},
            html.input({
                "type": "date", 
                "class": "input-field", 
                "value": fecha, 
                "on_change": actualizar_fecha,
                "style": {"width": "200px"}
            }),
            html.button(
                {
                    "class": "button-secondary",
                    "on_click": buscar_hoteles,
                    "disabled": buscando
                }, 
                [
                    "Buscar hoteles",
                    html.span({"class": "loading"}) if buscando else None
                ]
            )
        ),
        
        html.div({"style": {"color": "#ffcccc", "margin": "10px 0"}}, error) if error else None,
        
        
        html.div(
            {"class": "results-container"},
            html.h3("Hoteles disponibles para la fecha seleccionada:"),
            html.ul(
                {"class": "hotel-list"},
                [html.li({"class": "hotel-item"}, hotel) for hotel in hoteles]
            ) if hoteles else html.p("No se han encontrado hoteles disponibles para esta fecha")
        ) if (hoteles or not buscando) and not error else None,
        
        
        html.a(
            {
                "href": "/tarifas",
                "class": "button-blue nav-link",
                "style": {"display": "block", "width": "200px", "margin": "20px auto"}
            }, 
            "Continuar a Tarifas"
        ) if hoteles else None
    )

@component
def Tarifas():
    personas, set_personas = use_state(1)
    tipo, set_tipo = use_state("economica")
    resultado, set_resultado = use_state("")
    
    def actualizar_personas(e):
        set_personas(e["target"]["value"])
    
    def actualizar_tipo(e):
        set_tipo(e["target"]["value"])
    
    def consultar_tarifa(e):
        # Simulamos una respuesta de API
        set_resultado(f"Tarifa para {personas} personas, tipo {tipo}: $150")
    
    return html.div(
        {"class": "container-orange"},
        html.h1("Consulta de Tarifas"),
        html.p("Introduce los datos para calcular la tarifa."),
        html.input({
            "type": "number", 
            "placeholder": "Personas", 
            "class": "input-field",
            "value": personas,
            "on_change": actualizar_personas,
            "min": 1,
            "max": 10
        }),
        html.select(
            {
                "class": "input-field",
                "value": tipo,
                "on_change": actualizar_tipo
            },
            html.option({"value": "economica"}, "Económica"),
            html.option({"value": "lujo"}, "Lujo")
        ),
        html.button(
            {
                "class": "button-orange",
                "on_click": consultar_tarifa
            }, 
            "Consultar"
        ),
        html.div({"class": "results-container"}, resultado) if resultado else "",
        html.a(
            {
                "href": "/",
                "class": "button-blue nav-link"
            }, 
            "Volver al inicio"
        )
    )

# Componente principal para manejo de rutas
@component
def App():
    routes = [
        route("/", Layout(Bienvenida())),
        route("/disponibilidad", Layout(Disponibilidad())),
        route("/tarifas", Layout(Tarifas())),
        route("*", Layout(PageNotFound()))
    ]
    
    return browser_router(*routes)

# Para compatibilidad
@component
def SimpleApp():
    return html.div(
        {"style": {"padding": "20px"}},
        html.h1("Sistema de Reservas Hoteleras"),
        html.p("Bienvenido a nuestro sistema de reservas."),
        html.a({"href": "/disponibilidad"}, "Ver disponibilidad"),
        html.span(" | "),
        html.a({"href": "/tarifas"}, "Consultar tarifas")
    )