import requests
from PIL import Image
from io import BytesIO

url = "https://v3.football.api-sports.io/teams"
league_id = 128  # ID de la liga argentina
payload = {
    "league": league_id,
    "season": 2023
}

headers = {
    "x-rapidapi-key": "ea4550b62906e6b4a627ad666d52394f",
    "x-rapidapi-host": "v3.football.api-sports.io"
}

response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    equipos = data['response']
    equipo_buscado = input("Ingrese el nombre del equipo del cual desea ver el escudo: ").lower()

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

##MODULARIZADO Y FUNCIONANDO EN LLAMADOS_A_LA_API