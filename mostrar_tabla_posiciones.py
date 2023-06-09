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
    equipos = data
    print(equipos)
    # for equipo in equipos:
    #     posicion = equipo[0]['league']['standings']['rank']
    #     nombre_equipo = equipo['league']['standings']['team']['name']
    #     puntos = equipo['league']['standings']['points']
        
    #     print(f'{posicion}- {nombre_equipo} | {puntos}')
    
else:
    print('Error en la solicitud:', response.status_code)
