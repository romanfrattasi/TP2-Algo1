import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

payload = {
    'league':128,
    'season':2023
}

HEADERS = {
        "x-rapidapi-key": "09d1ab5e3cf7f087a82915004a769d76",
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

ids_equipos=  {'Gimnasia L.P.': 434,
               'River Plate': 435,
               'Racing Club': 436,
               'Rosario Central': 437,
               'Velez Sarsfield': 438,
               'Godoy Cruz': 439,
               'Belgrano Cordoba': 440,
               'Union Santa Fe': 441,
               'Defensa Y Justicia': 442,
               'Huracan': 445,
               'Lanus': 446,
               'Colon Santa Fe': 448,
               'Banfield': 449,
               'Estudiantes L.P.': 450,
               'Boca Juniors': 451,
               'Tigre': 452,
               'Independiente': 453,
               'Atletico Tucuman': 455,
               'Talleres Cordoba': 456,
               'Newells Old Boys': 457,
               'Argentinos JRS': 458,
               'Arsenal Sarandi': 459,
               'San Lorenzo': 460,
               'Sarmiento Junin': 474,
               'Instituto Cordoba': 478,
               'Platense': 1064,
               'Central Cordoba de Santiago': 1065,
               'Barracas Central': 2432}

#PRE:
#POST:
def llamado_api(url: str, payload: dict, headers: dict):
    response = requests.get(url, headers=headers, params=payload)
    return response

#PRE:
#POST: Devuelve el equipo elegido por el usuario.
def pedir_equipo(ids_equipos: dict) -> str:
    for equipo in ids_equipos.keys():
        print(f"{equipo}")
    equipo = input("Escriba el equipo deseado: ").title()
    while equipo not in ids_equipos:
        equipo = input("El equipo no es correcto, intente nuevamente: ").title()
    return equipo

#PRE:
#POST:
def modificar_payload(equipo: str, payload: dict) ->dict:
    payload.update({'team':ids_equipos[equipo]})
    return payload

#PRE:
#POST: Muestra un gráfico de los goles anotados de un equipo por minuto.
def imprimir_grafico(ids_equipos: dict, payload: dict) -> None:
    equipo_deseado = pedir_equipo(ids_equipos)
    payload = modificar_payload(equipo_deseado, payload)
    response = llamado_api("https://v3.football.api-sports.io/teams/statistics", payload, HEADERS)
    if response.status_code == 200:
        data = response.json()
        equipos:dict = data['response']
        eje_X = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']
        eje_Y = [equipos["goals"]["for"]["minute"][minutos]["total"] for minutos in eje_X]
        plt.plot(eje_X, eje_Y)
        plt.show()
    else:
        print("Error en la solicitud de equipos:", response.status_code)
    del payload["team"]

#PRE:
#POST:
def mostrar_escudo_e_informacion(payload: dict, ids_equipos: dict) ->None:
    response = llamado_api("https://v3.football.api-sports.io/teams", payload, HEADERS)
    if response.status_code == 200:
        data = response.json()
        equipos = data['response']
        equipo_buscado = pedir_equipo(ids_equipos)
        for equipo in equipos:
            cancha = equipo['venue']['name']
            ciudad_cancha = equipo['venue']['city']
            direccion_cancha = equipo['venue']['address']
            capacidad = equipo['venue']['capacity']
            nombre_equipo = equipo['team']['name']
            escudo_url = equipo['team']['logo']
            if nombre_equipo.lower() == equipo_buscado.lower():
                response = requests.get(escudo_url)
                if response.status_code == 200:
                    print(f"El nombre del estadio del equipo {nombre_equipo} es: {cancha}, ubicado en la ciudad de {ciudad_cancha}, en la dirección {direccion_cancha}, el cual cuenta con una capacidad de {capacidad} espectadores.")
                    imagen_de_escudo = Image.open(BytesIO(response.content))
                    imagen_de_escudo.show()
                else:
                    print("Error al obtener el escudo:", response.status_code)
    else:
        print("Error en la solicitud de equipos:", response.status_code)

#PRE:
#POST:
def pedir_temporada() ->int:
    temporada = None
    while temporada is None:
        try:
            temporada = int(input("Por favor ingrese la temporada: "))
            
        except ValueError:
            print("Ingreso erróneo. Intenta de nuevo.")
    return temporada

#PRE:
#POST:
def mostrar_tabla_de_posiciones() ->None:
    payload_de_posiciones = {
    "league": 128,
    "season": pedir_temporada()
    }
    response = llamado_api("https://v3.football.api-sports.io/standings", payload_de_posiciones, HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data['results'] > 0: 
            if payload_de_posiciones['season']==2023:   
                posiciones = data['response'][0]['league']['standings'][1]
            else:
                posiciones= data['response'][0]['league']['standings'][0]
            
            print("Tabla de Posiciones:")
            for posicion in posiciones:
                nombre_equipo = posicion['team']['name']
                posicon_equipo = posicion['rank']
                puntos = posicion['points']
                print(f'{posicon_equipo}- {nombre_equipo} | {puntos}')
        else:
            print("No se encontraron datos de la tabla de posiciones.")
    else:
        print("Error en la solicitud:", response.status_code)

#PRE:
#POST:
def mostrar_jugadores(payload: dict, headers: dict, ids_equipos: dict) ->None:
    response = llamado_api("https://v3.football.api-sports.io/teams", payload, HEADERS)
    if response.status_code == 200:
        data = response.json()
        equipos = data['response']
        equipo_buscado = pedir_equipo(ids_equipos)
        for equipo in equipos:
            nombre_equipo = equipo['team']['name']
            equipo_id = equipo['team']['id']
            if nombre_equipo == equipo_buscado:
                payload_jugador = {"team": equipo_id, "season": 2023}
                print(f"Equipo: {nombre_equipo}")
                print("Jugadores:")
                url_jugador = "https://v3.football.api-sports.io/players"
                response_jugador = requests.get(url_jugador, headers=headers, params=payload_jugador)
                if response_jugador.status_code == 200:
                    jugadores = response_jugador.json()['response']
                    for jugador in jugadores:
                        nombre_jugador = jugador['player']['name']
                        posicion = jugador['statistics'][0]['games']['position']
                        print(f"- {nombre_jugador} ({posicion})")
                else:
                    print("Error en la solicitud de jugadores:", response_jugador.status_code)
    else:
        print("Error en la solicitud de equipos:", response.status_code)
mostrar_tabla_de_posiciones()
