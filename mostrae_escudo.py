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
    "x-rapidapi-key": "d0b3d415d1b1ae06f1698e7fcb0a3943",
    "x-rapidapi-host": "v3.football.api-sports.io"
}

response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    equipos = data['response']

    equipo_buscado = input("Ingrese el nombre del equipo del cual desea ver el escudo: ")

    for equipo in equipos:
        nombre_equipo = equipo['team']['name']
        escudo_url = equipo['team']['logo']
        if nombre_equipo.lower() == equipo_buscado.lower():
            response = requests.get(escudo_url)
            if response.status_code == 200:
                imagen_de_escudo = Image.open(BytesIO(response.content))
                imagen_de_escudo.show()
            else:
                print("Error al obtener el escudo:", response.status_code)
            
    else:
        print("Equipo no encontrado.")

else:
    print("Error en la solicitud de equipos:", response.status_code)
