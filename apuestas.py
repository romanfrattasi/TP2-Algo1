import requests

url = "https://v3.football.api-sports.io/fixtures"
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
    equipo_deseado = input("Escriba el equipo: ").title()
    fixtures = data['response']
    lista_partidos=[]
    for partido in fixtures:
        local = partido["teams"]["home"]["name"]
        visitante = partido["teams"]["away"]["name"]
        if local == equipo_deseado:
            partido= str((f"{local} vs {visitante}"))
            lista_partidos.append(partido)
        #elif visitante == equipo_deseado:
        #    partido= str((f"{local} vs {visitante}"))
        #    lista_partidos.append(partido)
    for i in range(len(lista_partidos)):
        print(f"{i+1}) {lista_partidos[i]}")
    posicion_partido_deseado=int((input("escoge el numero del partido a apostar: ")))-1
    print(f"{lista_partidos[posicion_partido_deseado]}")
else:
    print("Error en la solicitud de partidos:", response.status_code)
