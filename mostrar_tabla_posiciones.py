import requests
url = "https://v3.football.api-sports.io/standings"
league_id = 128  # ID de la liga argentina
payload = {
    "league": league_id,
    "season": 2021
}

headers = {
    "x-rapidapi-key": "d0b3d415d1b1ae06f1698e7fcb0a3943",
    "x-rapidapi-host": "v3.football.api-sports.io"
}
response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    if data['results'] > 0:
        posiciones = data['response'][0]['league']['standings'][0]

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