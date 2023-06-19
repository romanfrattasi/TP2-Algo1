import buscar_usuarios, llamados_a_la_api
import csv
from passlib.hash import pbkdf2_sha256

#PRE:
#POST:
def verificar_constrasenia(nombre_usuario,contrasenia)->str:
    lista_usuarios=[]
    lista_contrasenias=[]
    contador_de_iteracion=0
    with open("usuarios.csv", 'r', newline='') as usuarios:
        contador_de_iteracion=1
        lector_csv = csv.reader(usuarios)
        for linea in lector_csv:
            if contador_de_iteracion <=1:
                contador_de_iteracion=contador_de_iteracion+1
            else:
                lista_contrasenias.append(linea[2])
                lista_usuarios.append(linea[1])
            
    for i in range(len(lista_usuarios)):
        if nombre_usuario == lista_usuarios[i]:
            while not pbkdf2_sha256.verify(contrasenia, lista_contrasenias[i]):
                contrasenia=input("Error, esta no es la contrasenia correcta, intentelo otra vez: ")
            if  pbkdf2_sha256.verify(contrasenia, lista_contrasenias[i]):
                return contrasenia

#PRE:
#POST:
def ingreso_usuario()->str:
    nombre_usuario = input('Ingresa tu nombre de usuario: ')
    datos_usuario=[]
    with open("usuarios.csv", 'r', newline='') as usuarios:
        lista_usuario=[]
        datos = [usuario.splitlines() for usuario in usuarios][1:]
        for i in range(len(datos)):
            partes = datos[i][0].split(',')
            partes=partes[:2]
            datos_usuario.append(partes)
    for i in range(len(datos_usuario)):
        lista_usuario.append(datos_usuario[i][1])
    while nombre_usuario not in lista_usuario:
        nombre_usuario =input('El usuario que acabas de escribir no existe: ')
    contrasena = input('Ingresa tu contraseña: ')
    contrasena=verificar_constrasenia(nombre_usuario,contrasena)
    return nombre_usuario

#PRE:
#POST:
def verificar_usuario_o_mail(usuario_o_mail, posicion_en_archivo, string)->str:
    datos_usuario = []
    with open("usuarios.csv", 'r', newline='') as usuarios:
        lista_usuario_o_mail = []
        datos = [usuario.splitlines() for usuario in usuarios][1:]
        for i in range(len(datos)):
            partes = datos[i][0].split(',')
            partes = partes[:2]
            datos_usuario.append(partes)
    for i in range(len(datos_usuario)):
        lista_usuario_o_mail.append(datos_usuario[i][posicion_en_archivo])
        
    while usuario_o_mail in lista_usuario_o_mail:
        usuario_o_mail = input(f'Este {string} ya está ocupado, escribe otro: ')
    return usuario_o_mail

#PRE:
#POST:
def registro_usuario()->str:
    email = input('Ingresa tu email: ')
    email = verificar_usuario_o_mail(email, 0, "email")  
    nombre_usuario = input('Ingresa tu nombre de usuario: ')
    nombre_usuario = verificar_usuario_o_mail(nombre_usuario, 1, "nombre de usuario")  
    contrasena = input('Ingresa tu contraseña: ')
    hash_contrasena = pbkdf2_sha256.hash(contrasena)
    with open("usuarios.csv", 'a', newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow([email, nombre_usuario, hash_contrasena, 0.0, None, 0.0])
    return nombre_usuario

def menu_bienvenida()->str:
    print('BIENVENIDO')
    opcion = ''
    while opcion != '0' and opcion != '1':
        opcion = input('Pulse 0 para ingresar a su cuenta o 1 para registrarse: ')
        if opcion != '0' and opcion != '1':
            print("Opción inválida. Intenta nuevamente.")
    if opcion == '0':
        nombre_usuario = ingreso_usuario()
    elif opcion == '1':
        nombre_usuario = registro_usuario()
    return nombre_usuario

##############################

def menu(OPCIONES):
    opciones_validas = '123456789'
    
    for i in range(len(OPCIONES)):
        print(f'{i+1}- {OPCIONES[i]}')
    opcion = input('Elija una opcion: ')
    
    while opcion not in opciones_validas:
        print('Opcion incorrecta. Intente otra vez')
        for i in range(len(OPCIONES)):
            print(f'{i+1}- {OPCIONES[i]}')
        opcion = input('Elija una opcion: ')
    
    return opcion

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
    
    nombre_usuario = menu_bienvenida()
    opcion = menu(OPCIONES)
    
    while opcion != '9':
        if opcion == '1':
            llamados_a_la_api.mostrar_jugadores(payload, HEADERS, ids_equipos)
        elif opcion =='2':
            llamados_a_la_api.mostrar_tabla_de_posiciones(HEADERS)
        elif opcion =='3':
            llamados_a_la_api.mostrar_escudo_e_informacion(payload, ids_equipos, HEADERS)
        elif opcion =='4':
            llamados_a_la_api.imprimir_grafico(ids_equipos, payload, HEADERS)
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
            buscar_usuarios.usuario_mas_ganador()
        elif opcion =='8':
            dinero_disponible = buscar_usuarios.obtener_dinero_disponible(nombre_usuario)
            llamados_a_la_api.comenzar_sistema_apuestas(HEADERS, nombre_usuario, dinero_disponible)
        
        opcion = menu(OPCIONES)
        
main()