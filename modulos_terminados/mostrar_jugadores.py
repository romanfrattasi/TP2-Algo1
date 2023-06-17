import requests
url = "https://v3.football.api-sports.io/teams"
league_id = 128  # ID de la liga argentina
payload = {
    "league": league_id,
    "season": 2023
}

headers = {
    "x-rapidapi-key": "09d1ab5e3cf7f087a82915004a769d76",
    "x-rapidapi-host": "v3.football.api-sports.io"
}
response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    equipos = data['response']
    lista_equipos = [equipo['team']['name'] for equipo in equipos]
    lista_equipos.sort()
    for equipo in lista_equipos:
        print(equipo)
    equipo_buscado = input("Ingrese el nombre del equipo del cual desea ver los jugadores: ")

    for equipo in equipos:
        nombre_equipo = equipo['team']['name']
        equipo_id = equipo['team']['id']
        if nombre_equipo.lower() == equipo_buscado.lower():
            print(f"Equipo: {nombre_equipo}")
            print("Jugadores:")
            url_jugador = "https://v3.football.api-sports.io/players"
            payload_jugador = {
                "team": equipo_id,
                "season": 2023
            }
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

##MODULARIZADO Y FUNCIONANDO EN LLAMADOS_A_LA_API

