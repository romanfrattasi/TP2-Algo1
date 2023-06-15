import requests
url = "https://v3.football.api-sports.io/teams"

payload={
    "league": 128,
    "season": 2023
}
headers = {
  'x-rapidapi-key': 'd0b3d415d1b1ae06f1698e7fcb0a3943',
  'x-rapidapi-host': 'v3.football.api-sports.io'
}

response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    equipos = data['response']
    
    for equipo in equipos:
        nombre_equipo = equipo['team']['name']
        estadio = equipo['venue']['name']
        ciudad = equipo['venue']['city']
        
        print(f"Equipo: {nombre_equipo}")
        print(f'Estadio: {estadio}')
        print(f'Ciudad: {ciudad}')
        print('------')
else:
    print('Error en la solicitud:', response.status_code)



