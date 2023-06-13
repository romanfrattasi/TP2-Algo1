import requests
import matplotlib.pyplot as plt

<<<<<<< HEAD
equipo = 435

url = "https://v3.football.api-sports.io/teams/statistics"
=======
url = "https://v3.football.api-sports.io/teams"
>>>>>>> 826bf5668538cf68b7f2e489b3660f78306b843d
league_id = 128  # ID de la liga argentina

payload = {
    "league": league_id,
<<<<<<< HEAD
    "season": 2023,
    "team":equipo
}
# llave de roman = d0b3d415d1b1ae06f1698e7fcb0a3943
headers = {
    "x-rapidapi-key": "ea4550b62906e6b4a627ad666d52394f",
=======
    "season": 2023
}

headers = {
    "x-rapidapi-key": "d0b3d415d1b1ae06f1698e7fcb0a3943",
>>>>>>> 826bf5668538cf68b7f2e489b3660f78306b843d
    "x-rapidapi-host": "v3.football.api-sports.io"
}

response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    equipos = data['response']
<<<<<<< HEAD
    print(data)
=======

>>>>>>> 826bf5668538cf68b7f2e489b3660f78306b843d
    equipo_buscado = input("Ingrese el nombre del equipo: ")

    equipo_id = None
    for equipo in equipos:
        nombre_equipo = equipo['team']['name']
        if nombre_equipo.lower() == equipo_buscado.lower():
            equipo_id = equipo['team']['id']
            break

    if equipo_id:
        player_url = f"https://v3.football.api-sports.io/players?team={equipo_id}&season=2023"
        player_response = requests.get(player_url, headers=headers)

        if player_response.status_code == 200:
            players = player_response.json()['response']

            goles_minutos = []
            for player in players:
                goles = player['statistics'][0]['goals']['total']
                minutos = player['statistics'][0]['games']['minutes']
                if goles is not None and minutos is not None:
                    goles_minutos.append((goles, minutos))

            goles_minutos.sort(key=lambda x: x[1])  # Ordenar por minutos jugados

            goles = [x[0] for x in goles_minutos]
            minutos = [x[1] for x in goles_minutos]

            plt.plot(minutos, goles)
            plt.xlabel("Minutos jugados")
            plt.ylabel("Goles realizados")
            plt.title(f"Goles vs. Minutos para el equipo {equipo_buscado} - Temporada 2023")

            # Establecer los ticks en el eje x en incrementos de 10 minutos
            plt.xticks(range(0, 91, 10))

            plt.show()
        else:
            print("Error en la solicitud de jugadores:", player_response.status_code)
    else:
        print("Equipo no encontrado.")
else:
<<<<<<< HEAD
    print("Error en la solicitud de equipos:", response.status_code)
=======
    print("Error en la solicitud de equipos:", response.status_code)
>>>>>>> 826bf5668538cf68b7f2e489b3660f78306b843d
