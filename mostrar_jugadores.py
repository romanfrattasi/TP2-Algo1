import requests
url = "https://v3.football.api-sports.io/teams"
league_id = 128  # ID de la liga argentina
payload = {
    "league": league_id,
    "season": 2023
}

headers = {
    "x-rapidapi-key": "d0b3d415d1b1ae06f1698e7fcb0a3943",
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
            player_url = "https://v3.football.api-sports.io/players"
            player_payload = {
                "team": equipo_id,
                "season": 2023
            }
            player_response = requests.get(player_url, headers=headers, params=player_payload)
            if player_response.status_code == 200:
                players = player_response.json()['response']
                for player in players:
                    nombre_jugador = player['player']['name']
                    posicion = player['statistics'][0]['games']['position']
                    print(f"- {nombre_jugador} ({posicion})")
            else:
                print("Error en la solicitud de jugadores:", player_response.status_code)
else:
    print("Error en la solicitud de equipos:", response.status_code)
