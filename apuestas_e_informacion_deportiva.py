import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from random import randint
import modificar_y_leer_archivoscsv

#PRE: Recibe la url y los diccionarios a utilizar para el llamado.
#POST: Devuelve un archivo json.
def llamado_api(url: str, payload: dict, headers: dict):
    response = requests.get(url, headers=headers, params=payload)
    return response

#PRE: Recibe el nombre de un equipo.
#POST: Modifica el nombre del equipo en caso de ser necesario.
def modificar_nombre_de_equipos_problemáticos(nombre_de_equipo: str) -> str:
    if nombre_de_equipo == "Central Cordoba De Santiago":
        nombre_de_equipo = "Central Cordoba de Santiago"
    elif nombre_de_equipo == "Argentinos Jrs":
        nombre_de_equipo = "Argentinos JRS"
    return nombre_de_equipo

#PRE:
#POST: Devuelve el equipo elegido por el usuario.
def pedir_equipo(ids_equipos: dict) -> str:
    for equipo in ids_equipos.keys():
        print(f"{equipo}")
    equipo = input("🔵 Escriba el equipo deseado: ").title()
    while equipo not in ids_equipos:
        equipo = input("🔴 El equipo no es correcto, intente nuevamente: ").title()
    equipo = modificar_nombre_de_equipos_problemáticos(equipo)
    return equipo

#PRE: Recibe el diccionario con todos los equipos, el equipo seleccionado y el payload a modificar.
#POST: Agrega una llave al diccionario y lo devuelve.
def modificar_payload(equipo: str, payload: dict, ids_equipos: dict) ->dict:
    payload.update({'team':ids_equipos[equipo]})
    return payload

#PRE:
#POST: Muestra un gráfico de los goles anotados de un equipo por minuto.
def imprimir_grafico(ids_equipos: dict, payload: dict, HEADERS) -> None:
    equipo_deseado = pedir_equipo(ids_equipos)
    payload = modificar_payload(equipo_deseado, payload, ids_equipos)
    response = llamado_api("https://v3.football.api-sports.io/teams/statistics", payload, HEADERS)
    if response.status_code == 200:
        data = response.json()
        equipos:dict = data['response']
        eje_X = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']
        eje_Y = [equipos["goals"]["for"]["minute"][minutos]["total"] for minutos in eje_X]
        plt.plot(eje_X, eje_Y)
        plt.show()
    else:
        print("Error en la solicitud.", response.status_code)
    del payload["team"]

#PRE: Recibe el payload y headers para llamar a la api, junto con el diccionario de todos los equipos.
#POST: Muestra la información del equipo, su estadio y escudo.
def mostrar_escudo_e_informacion(payload: dict, ids_equipos: dict, HEADERS) ->None:
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
                    print(f"🟢 El nombre del estadio del equipo {nombre_equipo} es: {cancha}, ubicado en la ciudad de {ciudad_cancha}, en la dirección {direccion_cancha}, el cual cuenta con una capacidad de {capacidad} espectadores.")
                    imagen_de_escudo = Image.open(BytesIO(response.content))
                    imagen_de_escudo.show()
                else:
                    print("Error al obtener los datos del equipo:", response.status_code)
    else:
        print("Error en la solicitud.", response.status_code)

#PRE:
#POST: Devuelve la temporada elegida.
def pedir_temporada() ->int:
    temporada = None
    while temporada is None:
        try:
            temporada = int(input("🔵 Por favor ingrese la temporada (2015 a 2023): "))
        except ValueError:
            print("🔴 Ingreso erróneo. Intentá de nuevo.")
    return temporada

#PRE: Recibe el diccionario de headers para hacer llamado a la api.
#POST: Muestra la tabla de posiciones de la temporada elegida.
def mostrar_tabla_de_posiciones(HEADERS: dict) ->None:
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
        print("Error en la solicitud.", response.status_code)

#PRE: Recibe payload y headers para el llamado a la api, junto con el diccionario de todos los equipos.
#POST: Muestra el plantel del equipo elegido.
def mostrar_jugadores(payload: dict, HEADERS: dict, ids_equipos: dict) ->None:
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
                response_jugador = llamado_api(url_jugador, payload_jugador, HEADERS)
                if response_jugador.status_code == 200:
                    jugadores = response_jugador.json()['response']
                    for jugador in jugadores:
                        nombre_jugador = jugador['player']['name']
                        posicion = jugador['statistics'][0]['games']['position']
                        print(f"- {nombre_jugador} ({posicion})")
                else:
                    print("Error en la solicitud de jugadores.", response_jugador.status_code)
    else:
        print("Error en la solicitud.", response.status_code)

#PRE:
#POST: Devuelve la fecha o el partido.
def pedir_fecha_o_partido_a_apostar() -> int:
    fecha_o_partido = None
    while fecha_o_partido is None:
        try:
            fecha_o_partido = int(input("🟠 Ingrese el número: "))
        except ValueError:
            print("🔴 Incorrecto, intente nuevamente: ")
    return fecha_o_partido

#PRE:
#POST: Verifica que el partido este en el rango correspondiente
def verificar_partido_existente(partido: int) -> int:
    while(partido < 1 or partido > 14):
        print("Incorrecto. Intenta nuevamente.")
        partido = pedir_fecha_o_partido_a_apostar() 
    return partido - 1

#PRE: Se reciben los equipos.
#POST: Devuelve el equipo ganador.
def calcular_ganador(equipo_local: str,equipo_visitante: str) -> str:
    dado = randint(1,3)
    equipo_ganador = ''
    if dado == 1:
        equipo_ganador = equipo_local
    elif dado == 2:
        equipo_ganador = 'Empate'
    elif dado == 3:
        equipo_ganador = equipo_visitante
    return equipo_ganador

#PRE: Recibe un diccionario con todas las fechas.
#POST: Devuelve una tupla compuesta por una lista de partidos, y un diccionario con el id de cada encuentro.
def organizar_partidos_por_fecha(fixtures: dict) -> tuple:
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

#PRE:
#POST: Imprime todos los partidos de la fecha.
def mostrar_partidos_por_pantalla(lista_partidos_por_fecha: list) -> None:
    for i in range(len(lista_partidos_por_fecha)):
        print(f"{i+1}) {lista_partidos_por_fecha[i]}")

#PRE: Se recibe lista con todos los partidos y diccionario con los id's de cada uni.
#POST: Devuelve el id del partido elegido.
def seleccion_partido(lista_partidos_por_fecha: list, diccionario_id_partidos: dict) -> int:
    print("🟠 Elija el partido por el que quiere apostar.")
    indice_de_partido = pedir_fecha_o_partido_a_apostar()
    indice_de_partido = verificar_partido_existente(indice_de_partido)
    print(f"Usted quiere apostar al partido de {lista_partidos_por_fecha[indice_de_partido]}")
    id_del_partido_seleccionado=diccionario_id_partidos[lista_partidos_por_fecha[indice_de_partido]]
    return id_del_partido_seleccionado

#PRE: Se reciben los equipos y el booleano que indica el posible ganador.
#POST: Devuelve una tupla con el posible ganador y perdedor
def buscar_posible_ganador(equipo_local: str, equipo_visitante: str, win_or_draw: bool) -> tuple:
    posible_ganador = equipo_local if win_or_draw else equipo_visitante #equipo que tiene win_or_draw = True
    posible_perdedor = equipo_local if not win_or_draw else equipo_visitante #equipo que tiene win_or_draw = False
    return posible_ganador, posible_perdedor

#PRE: Recibe el posible ganador y perdedor, junto con el monto a apostar.
#POST: Devuelve una tupla con las posibles ganancias.
def posibles_ganancias(posible_ganador: str, posible_perdedor:str, dinero_a_apostar: float) -> tuple:
    coste_apuesta = randint(1,4)
    posible_ganancia_alta = dinero_a_apostar + (dinero_a_apostar * coste_apuesta)
    posible_ganancia_baja = dinero_a_apostar + ((coste_apuesta/10)*dinero_a_apostar)
    posible_ganancia_empate = dinero_a_apostar * 1.5
    print(f'Si el ganador es {posible_ganador} ganaras ${posible_ganancia_baja} 💸')
    print(f'Si empatan ganaras ${posible_ganancia_empate} 💸💸')
    print(f'Si el ganador es {posible_perdedor} ganaras ${posible_ganancia_alta} 💸💸💸')
    return posible_ganancia_alta, posible_ganancia_baja, posible_ganancia_empate

#PRE: Se recibe el dinero disponible.
#POST: Devuelve el monto a apostar.
def ingresar_apuesta(dinero_disponible: float) -> float:
    apuesta = None
    while apuesta is None:
        try:
            apuesta = float(input('¿Cuanto dinero deseas apostar?: '))
            while apuesta > dinero_disponible or apuesta <= 0:
                print(f'🔴 El monto ingresado no es valido. Tenes ${dinero_disponible} disponibles para apostar')
                apuesta = None
                apuesta = float(input('¿Cuanto dinero deseas apostar?: '))
        except ValueError:
            print('🔴 El monto ingresado no es valido. Intenta de nuevo.')
    return apuesta

#PRE: Se recibe el fixture, nombre de usuario y el dinero disponible.
#POST: Se realiza la apuesta, se indica el resultado, y se actualizan los archivos de usuarios y transacciones.
def apostar(fixtures: dict, nombre_usuario: str, dinero_disponible: float) -> None:
    equipo_local = fixtures[0]['teams']['home']['name']
    equipo_visitante = fixtures[0]['teams']['away']['name']
    win_or_draw = fixtures[0]["predictions"]["win_or_draw"]
    posible_ganador, posible_perdedor = buscar_posible_ganador(equipo_local, equipo_visitante, win_or_draw)
    dinero_a_apostar = ingresar_apuesta(dinero_disponible)
    dinero_disponible -= dinero_a_apostar
    posible_ganancia_alta, posible_ganancia_baja, posible_ganancia_empate = posibles_ganancias(posible_ganador, posible_perdedor, dinero_a_apostar)
    equipo_que_deseas_apostar = input("🟠 Escribe el equipo por el que deseas apostar (o sino escribe Empate): ").title() 
    while equipo_que_deseas_apostar != equipo_local and equipo_que_deseas_apostar != equipo_visitante and equipo_que_deseas_apostar != 'Empate':
        print('🔴 La opcion ingresada no es correcta')
        equipo_que_deseas_apostar = input("Escribe el equipo que deseas apostar: ").title()
    equipo_ganador = calcular_ganador(equipo_local,equipo_visitante)
    if equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == posible_ganador:
        print(f'Felicitaciones! Ganaste ${posible_ganancia_baja} 💸')
        dinero_disponible += posible_ganancia_baja
        modificar_y_leer_archivoscsv.cargar_a_csv_transacciones(dinero_a_apostar, nombre_usuario, 'Gana')
        modificar_y_leer_archivoscsv.cargar_datos_apuesta_a_csv_usuarios(dinero_disponible, nombre_usuario, dinero_a_apostar)
    elif equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == posible_perdedor:
        print(f'Felicitaciones! Ganaste ${posible_ganancia_alta} 💸💸💸')
        dinero_disponible += posible_ganancia_alta
        modificar_y_leer_archivoscsv.cargar_a_csv_transacciones(dinero_a_apostar, nombre_usuario, 'Gana')
        modificar_y_leer_archivoscsv.cargar_datos_apuesta_a_csv_usuarios(dinero_disponible, nombre_usuario, dinero_a_apostar)
    elif equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == 'Empate':
        print(f'Felicitaciones! Ganaste ${posible_ganancia_empate} 💸💸')
        dinero_disponible += posible_ganancia_empate
        modificar_y_leer_archivoscsv.cargar_a_csv_transacciones(dinero_a_apostar, nombre_usuario, 'Gana')
        modificar_y_leer_archivoscsv.cargar_datos_apuesta_a_csv_usuarios(dinero_disponible, nombre_usuario, dinero_a_apostar)
    else:
        print('Perdiste la apuesta 🫤')
        modificar_y_leer_archivoscsv.cargar_a_csv_transacciones(dinero_a_apostar, nombre_usuario, 'Pierde')
        modificar_y_leer_archivoscsv.cargar_datos_apuesta_a_csv_usuarios(dinero_disponible, nombre_usuario, dinero_a_apostar)

#PRE: Se recibe la jornada.
#POST: Verifica que la jornada este en el rango correspondiente y luego la devuelve.
def verificar_fecha_existente(jornada: int):
    while(jornada < 1 or jornada > 27):
        print("🔴 Incorrecto. Intentá nuevamente.")
        jornada = pedir_fecha_o_partido_a_apostar() 
    return jornada

#PRE: Se reciben los headers para llamar a la api, junto con el nombre de usuario y su dinero disponible.
#POST: Se desarrolla el flujo del sistema de apuestas.
def comenzar_sistema_apuestas(HEADERS: dict, nombre_usuario: str, dinero_disponible: float) -> None:
    print("🟠 Debe elegir la fecha en la cual quiere apostar. Debe ser entre la 1(inclusive) y la 27(inclusive).")
    jornada_a_buscar= pedir_fecha_o_partido_a_apostar()
    jornada_a_buscar = verificar_fecha_existente(jornada_a_buscar)
    jornada=str(jornada_a_buscar)
    round_a_buscar="1st Phase"+ " " + "-"+ " "+jornada
    payload_fecha ={"league":"128",
          "season": "2023",
          "round": round_a_buscar}
    url = "https://v3.football.api-sports.io/fixtures"
    response_fecha=llamado_api(url,payload_fecha,HEADERS)
    if response_fecha.status_code == 200:
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
        apostar(fixtures, nombre_usuario, dinero_disponible)
    else:
        print("No se encontraron partidos para la fecha especificada en la primera fase.")