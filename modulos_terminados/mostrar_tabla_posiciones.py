import requests
url = "https://v3.football.api-sports.io/standings"
league_id = 128  # ID de la liga argentina

temporada = None
while temporada is None:
    try:
        temporada = int(input("Por favor ingrese la temporada: "))
    except ValueError:
        print("Ingreso erróneo. Intenta de nuevo.")

payload = {
    "league": league_id,
    "season": temporada
}

headers = {
    "x-rapidapi-key": "09d1ab5e3cf7f087a82915004a769d76",
    "x-rapidapi-host": "v3.football.api-sports.io"
}
response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    if data['results'] > 0:
        posiciones = data['response'][0]['league']['standings'][1]

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
    
##MODULARIZADO Y FUNCIONANDO EN LLAMADOS_A_LA_API
