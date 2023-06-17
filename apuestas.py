import requests
from random import randint

dinero_disponible = 1000

url = "https://v3.football.api-sports.io/fixtures"
league_id = 128
temporada = 2023 
fecha = '2023-06-12'#input("Ingrese la fecha en formato AAAA-MM-DD: ")  


payload ={"league":"128",
          "season": "2023",
          "date": fecha}


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
            
            apuesta = float(input('¿Cuanto dinero deseas apostar?: '))
            dinero_disponible -= apuesta
            
            equipo_local = fixtures[0]['teams']['home']['name']
            equipo_visitante = fixtures[0]['teams']['away']['name']
            win_or_draw = fixtures[0]["predictions"]["win_or_draw"]
            posible_ganador = equipo_local if win_or_draw else equipo_visitante #equipo que tiene win_or_draw = True
            posible_perdedor = equipo_local if not win_or_draw else equipo_visitante #equipo que tiene win_or_draw = False
            
            coste_apuesta = randint(1,4)
            
            posible_ganancia_alta = apuesta + (apuesta * coste_apuesta)
            posible_ganancia_baja = apuesta + ((coste_apuesta/10)*apuesta)
            posible_ganancia_empate = apuesta * 1.5
            
            print(f'Si el ganador es {posible_ganador} ganaras ${posible_ganancia_baja}')
            print(f'Si el ganador es {posible_perdedor} ganaras ${posible_ganancia_alta}')
            print(f'Si empatan ganaras ${posible_ganancia_empate}')
            
            
            equipo_que_deseas_apostar = input("Escribe el equipo que deseas apostar (o Empate): ").title() #Agregar validaciones
            while equipo_que_deseas_apostar != equipo_local and equipo_que_deseas_apostar != equipo_visitante and equipo_que_deseas_apostar != 'Empate':
                print('La opcion ingresada no es correcta')
                equipo_que_deseas_apostar = input("Escribe el equipo que deseas apostar: ").title()
                
            dado = randint(1,3)
            equipo_ganador = ''
            
            if dado == 1:
                equipo_ganador = equipo_local
            elif dado == 2:
                equipo_ganador = 'Empate'
            elif dado == 3:
                equipo_ganador = equipo_visitante
                
            if equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == posible_ganador:
                print(f'Felicitaciones! Ganaste ${posible_ganancia_baja}')
                dinero_disponible += posible_ganancia_baja
            elif equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == posible_perdedor:
                print(f'Felicitaciones! Ganaste ${posible_ganancia_alta}')
                dinero_disponible += posible_ganancia_alta
            elif equipo_ganador == equipo_que_deseas_apostar and equipo_ganador == 'Empate':
                print(f'Felicitaciones! Ganaste ${posible_ganancia_empate}')
                dinero_disponible += posible_ganancia_empate
            else:
                print('Perdiste!')
            
            
    else:
        print("No se encontraron partidos para la fecha especificada en la primera fase")


else:
    print("Error en la solicitud de partidos:", response.status_code)
