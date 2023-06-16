import requests
from random import randint

url = "https://v3.football.api-sports.io/fixtures"
league_id = 128
temporada = 2023 
fecha = input("Ingrese la fecha en formato AAAA-MM-DD: ")  


payload ={"league":"128","season": "2023", "date": fecha}


headers = {
    "x-rapidapi-key": "ea4550b62906e6b4a627ad666d52394f",
    "x-rapidapi-host": "v3.football.api-sports.io"
}

response = requests.get(url, headers=headers, params=payload)

if response.status_code == 200:
    data = response.json()
    fixtures = data['response']
    lista_partidos_por_fecha=[]
    diccionario_id_partidos={}
    if fixtures:
        
        for partido in fixtures:
            local = partido["teams"]["home"]["name"]
            visitante = partido["teams"]["away"]["name"]
            id_partido=partido["fixture"]["id"]
            partido_a_jugar=f"{local} vs {visitante}"
            diccionario_id_partidos[partido_a_jugar]=id_partido
            lista_partidos_por_fecha.append(partido_a_jugar)
        
        for i in range(len(lista_partidos_por_fecha)):
            print(f"{i+1}) {lista_partidos_por_fecha[i]}")
        op=int(input("Elije el numero del partido que quieres apostar: "))-1
        print(f"Usted quiere apostar al partido de {lista_partidos_por_fecha[op]}")
        id_del_partido_seleccionado=diccionario_id_partidos[lista_partidos_por_fecha[op]]
        print(id_del_partido_seleccionado)
        payload_predicciones={
            "fixture":id_del_partido_seleccionado
        }
        nuevo_url="https://v3.football.api-sports.io/predictions"
        response_nuevo = requests.get(nuevo_url, headers=headers, params=payload_predicciones)
        if response_nuevo.status_code==200:
            data = response_nuevo.json()
            fixtures = data['response']
            dado=randint(1,4)
            equipo_que_deaseas_apostar=input("escribe el equipo que deseas apostar: ").title()
            gano_o_pierdo=fixtures[0]["predictions"]["win_or_draw"]
            print(gano_o_pierdo)
            
        
            #teniendo el partido, hay que entrar a fiixture y encontrar el id del partido y buscarla en el endpoint de predictons,
        
             #y luego sacamos el win or draw
            
    else:
        print("No se encontraron partidos para la fecha especificada en la primera fase")


else:
    print("Error en la solicitud de partidos:", response.status_code)
