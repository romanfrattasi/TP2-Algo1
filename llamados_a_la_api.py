import requests
import matplotlib.pyplot as plt



payload = {
    'league':128,
    'season':2023
}
ids_equipos=  {'Gimnasia L.P.': 434,
               'River Plate': 435,
               'Racing Club': 436,
               'Rosario Central': 437,
               'Velez Sarsfield': 438,
               'Godoy Cruz': 439,
               'Belgrano Cordoba': 440,
               'Union Santa Fe': 441,
               'Defensa Y Justicia': 442,
               'Huracan': 445,
               'Lanus': 446,
               'Colon Santa Fe': 448,
               'Banfield': 449,
               'Estudiantes L.P.': 450,
               'Boca Juniors': 451,
               'Tigre': 452,
               'Independiente': 453,
               'Atletico Tucuman': 455,
               'Talleres Cordoba': 456,
               'Newells Old Boys': 457,
               'Argentinos JRS': 458,
               'Arsenal Sarandi': 459,
               'San Lorenzo': 460,
               'Sarmiento Junin': 474,
               'Instituto Cordoba': 478,
               'Platense': 1064,
               'Central Cordoba de Santiago': 1065,
               'Barracas Central': 2432}

#PRE:
#POST:
def llamado_api(url: str, payload: dict):
    headers = {
        "x-rapidapi-key": "09d1ab5e3cf7f087a82915004a769d76",
        "x-rapidapi-host": "v3.football.api-sports.io"
    }


    response = requests.get(url, headers=headers, params=payload)
    return response

#PRE:
#POST: Devuelve el equipo elegido por el usuario.
def pedir_equipo(ids_equipos: dict) -> str:
    for equipo in ids_equipos.keys():
        print(f"{equipo}")
    equipo = input("Escribe el equipo deseado: ").title()
    while equipo not in ids_equipos:
        equipo = input("El equipo no es correcto, intente nuevamente: ").title()
    return equipo

def modificar_payload(equipo):
    payload.update({'team':ids_equipos[equipo]})
    return payload

#PRE:
#POST: Muestra un gráfico de los goles anotados de un equipo por minuto.
def imprimir_grafico(ids_equipos: dict) -> None:
    equipo_deseado = pedir_equipo(ids_equipos)
    payload = modificar_payload(equipo_deseado)
    response = llamado_api("https://v3.football.api-sports.io/teams/statistics", payload)
    if response.status_code == 200:
        data = response.json()
        equipos:dict = data['response']
        eje_X = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120']
        eje_Y = [equipos["goals"]["for"]["minute"][minutos]["total"] for minutos in eje_X]
        
        plt.plot(eje_X, eje_Y)
        plt.show()
    else:
        print("Error en la solicitud de equipos:", response.status_code)
        



imprimir_grafico(ids_equipos)