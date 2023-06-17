import ingreso, buscar_usuarios
import llamados_a_la_api

def menu(OPCIONES):
    nombre_usuario = ingreso.menu_bienvenida()
    opciones_validas = '123456789'
    
    for i in range(len(OPCIONES)):
        print(f'{i+1}- {OPCIONES[i]}')
    opcion = input('Elija una opcion: ')
    
    while opcion not in opciones_validas:
        print('Opcion incorrecta. Intente otra vez')
        for i in range(len(OPCIONES)):
            print(f'{i+1}- {OPCIONES[i]}')
        opcion = input('Elija una opcion: ')
    
    return opcion, nombre_usuario

def main():
    OPCIONES = ('Mostrar plantel',
                'Mostrar tabla de posiciones',
                'Mostrar informacion de un equipo',
                'Grafico goles/minutos',
                'Cargar dinero',
                'Mostrar el usuario que mas dinero aposto',
                'Mostrar el usuario que mas veces gano',
                'Apostar',
                'Salir'
                )
    HEADERS = {
        "x-rapidapi-key": "09d1ab5e3cf7f087a82915004a769d76",
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
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
    opcion, nombre_usuario = menu(OPCIONES)
    
    while opcion != '9':
        if opcion == '1':
            llamados_a_la_api.mostrar_jugadores(payload, HEADERS, ids_equipos)
        elif opcion =='2':
            llamados_a_la_api.mostrar_tabla_de_posiciones()
        elif opcion =='3':
            llamados_a_la_api.mostrar_escudo_e_informacion(payload, ids_equipos)
        elif opcion =='4':
            llamados_a_la_api.imprimir_grafico(ids_equipos, payload)
        elif opcion =='5':
            monto = None
            while monto is None:
                try :
                    monto = float(input('Ingresa el monto que deseas depositar: '))
                except ValueError:
                    print('El monto ingresado no es valido. Intenta de nuevo.')
            buscar_usuarios.cargar_dinero(monto, nombre_usuario)
        elif opcion =='6':
            buscar_usuarios.usuario_mas_apostador()
        elif opcion =='7':
            pass
        elif opcion =='8':
            llamados_a_la_api.comenzar_sistema_apuestas()
        
main()