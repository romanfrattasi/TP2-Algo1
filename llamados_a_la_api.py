import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from random import randint


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

def calcular_ganador(equipo_local,equipo_visitante):
    dado = randint(1,3)
    equipo_ganador = ''
    
    if dado == 1:
        equipo_ganador = equipo_local
    elif dado == 2:
        equipo_ganador = 'Empate'
    elif dado == 3:
        equipo_ganador = equipo_visitante
        
    return equipo_ganador
        
def organizar_partidos_por_fecha(fixtures):
    lista_partidos_por_fecha=[]
    diccionario_id_partidos={}
    for partido in fixtures:
        local = partido["teams"]["home"]["name"]
        visitante = partido["teams"]["away"]["name"]
        id_partido=partido["fixture"]["id"]
        partido_a_jugar=f"{local} vs {visitante}"
        diccionario_id_partidos[partido_a_jugar]=id_partido
        lista_partidos_por_fecha.append(partido_a_jugar)
    return lista_partidos_por_fecha, diccionario_id_partidos
    
def mostrar_partidos_por_pantalla(lista_partidos_por_fecha):
    for i in range(len(lista_partidos_por_fecha)):
        print(f"{i+1}) {lista_partidos_por_fecha[i]}")

def seleccion_partido(lista_partidos_por_fecha, diccionario_id_partidos):
    op=int(input("Elije el numero del partido que quieres apostar: "))-1
    print(f"Usted quiere apostar al partido de {lista_partidos_por_fecha[op]}")
    id_del_partido_seleccionado=diccionario_id_partidos[lista_partidos_por_fecha[op]]
    
    return id_del_partido_seleccionado

def buscar_posible_ganador(equipo_local, equipo_visitante, win_or_draw):
    posible_ganador = equipo_local if win_or_draw else equipo_visitante #equipo que tiene win_or_draw = True
    posible_perdedor = equipo_local if not win_or_draw else equipo_visitante #equipo que tiene win_or_draw = False
    return posible_ganador, posible_perdedor

def posibles_ganancias(posible_ganador, posible_perdedor, dinero_disponible):
    coste_apuesta = randint(1,4)
    apuesta = float(input('¿Cuanto dinero deseas apostar?: '))
    dinero_disponible -= apuesta
    
    posible_ganancia_alta = apuesta + (apuesta * coste_apuesta)
    posible_ganancia_baja = apuesta + ((coste_apuesta/10)*apuesta)
    posible_ganancia_empate = apuesta * 1.5
    
    print(f'Si el ganador es {posible_ganador} ganaras ${posible_ganancia_baja}')
    print(f'Si el ganador es {posible_perdedor} ganaras ${posible_ganancia_alta}')
    print(f'Si empatan ganaras ${posible_ganancia_empate}')
    
    return posible_ganancia_alta, posible_ganancia_baja, posible_ganancia_empate, dinero_disponible
    
def apostar(fixtures):
    dinero_disponible = 1000
    equipo_local = fixtures[0]['teams']['home']['name']
    equipo_visitante = fixtures[0]['teams']['away']['name']
    win_or_draw = fixtures[0]["predictions"]["win_or_draw"]
    posible_ganador, posible_perdedor = buscar_posible_ganador(equipo_local, equipo_visitante, win_or_draw)
    
    posible_ganancia_alta, posible_ganancia_baja, posible_ganancia_empate, dinero_disponible = posibles_ganancias(posible_ganador, posible_perdedor, dinero_disponible)
    
    equipo_que_deseas_apostar = input("Escribe el equipo que deseas apostar (o Empate): ").title() 
    
    while equipo_que_deseas_apostar != equipo_local and equipo_que_deseas_apostar != equipo_visitante and equipo_que_deseas_apostar != 'Empate':
        print('La opcion ingresada no es correcta')
        equipo_que_deseas_apostar = input("Escribe el equipo que deseas apostar: ").title()
    
    equipo_ganador = calcular_ganador(equipo_local,equipo_visitante)
    
    if equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == posible_ganador:
        print(f'Felicitaciones! Ganaste ${posible_ganancia_baja}')
        dinero_disponible += posible_ganancia_baja
    elif equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == posible_perdedor:
        print(f'Felicitaciones! Ganaste ${posible_ganancia_alta}')
        dinero_disponible += posible_ganancia_alta
    elif equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == 'Empate':
        print(f'Felicitaciones! Ganaste ${posible_ganancia_empate}')
        dinero_disponible += posible_ganancia_empate
    else:
        print('Perdiste!')


def comenzar_sistema_apuestas():
    payload_fecha ={"league":"128",
          "season": "2023",
          "date":  '2023-06-12'}
    url = "https://v3.football.api-sports.io/fixtures"
    response_fecha=llamado_api(url,payload_fecha,HEADERS)
    if response_fecha.status_code ==200:
        data = response_fecha.json()
        fixtures = data['response']
        if fixtures:
            lista_partidos_por_fecha, diccionario_id_partidos = organizar_partidos_por_fecha(fixtures)
            mostrar_partidos_por_pantalla(lista_partidos_por_fecha)
            id_del_partido_seleccionado = seleccion_partido(lista_partidos_por_fecha, diccionario_id_partidos)
            
            payload_predicciones={
                "fixture":id_del_partido_seleccionado
                }
            
            nuevo_url="https://v3.football.api-sports.io/predictions"
            response_nuevo = llamado_api(nuevo_url, payload_predicciones, HEADERS)
            
            data = response_nuevo.json()
            fixtures = data['response']
            
        apostar(fixtures)
        
    else:
        print("No se encontraron partidos para la fecha especificada en la primera fase")
comenzar_sistema_apuestas()

