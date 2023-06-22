import modificar_y_leer_archivoscsv, apuestas_e_informacion_deportiva
import csv
from passlib.hash import pbkdf2_sha256
import os

#PRE: Recibe un usuario y una contraseña.
#POST: Verifica que los parametros recibidos coincidan con el archivo, devuelve la contraseña en caso de que sea correcta.
def verificar_constrasenia(nombre_usuario: str,contrasenia: str)->str:
    lista_usuarios=[]
    lista_contrasenias=[]
    with open("usuarios.csv", 'r', newline='') as usuarios:
        ignorar_header=1
        lector_csv = csv.reader(usuarios)
        for linea in lector_csv:
            if ignorar_header == 1:
                ignorar_header=ignorar_header+1
            else:
                lista_contrasenias.append(linea[2])
                lista_usuarios.append(linea[1])
    for i in range(len(lista_usuarios)):
        if nombre_usuario == lista_usuarios[i]:
            while not pbkdf2_sha256.verify(contrasenia, lista_contrasenias[i]):
                contrasenia=input("🔴 Error, esta no es la contraseña correcta, inténtelo otra vez: ")
            if  pbkdf2_sha256.verify(contrasenia, lista_contrasenias[i]):
                return contrasenia

#PRE:
#POST: Valida el ingreso de usuario y contraseña, devuelve el nombre del usuario.
def ingreso_usuario()->str:
    nombre_usuario = input('🟢 Ingresá tu nombre de usuario: ')
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
        nombre_usuario =input('🔴 El usuario que acabas de escribir no existe, ingresalo nuevamente: ')
    contrasena = input('🟢 Ingresá tu contraseña: ')
    contrasena=verificar_constrasenia(nombre_usuario,contrasena)
    return nombre_usuario

#PRE:
#POST: Verifica que un mail o un usuario no este en uso, devuelve un usuario/mail que no exista en el archivo.
def verificar_usuario_o_mail_repetido(usuario_o_mail: str, posicion_en_archivo: int, formato: str)->str:
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
        usuario_o_mail = input(f'Este {formato} ya está ocupado, escribí otro: ')
    return usuario_o_mail

#PRE:
#POST: Registra un nuevo usuario o valida el ingreso de uno existente, devuelve el nombre del usuario.
def registro_usuario()->str:
    email = input('🟢 Ingresá tu email: ')
    email = verificar_usuario_o_mail_repetido(email, 0, "email")  
    nombre_usuario = input('🟢 Ingresá tu nombre de usuario: ')
    nombre_usuario = verificar_usuario_o_mail_repetido(nombre_usuario, 1, "nombre de usuario")  
    contrasena = input('🟢 Ingresá tu contraseña: ')
    hash_contrasena = pbkdf2_sha256.hash(contrasena)
    with open("usuarios.csv", 'a', newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow([email, nombre_usuario, hash_contrasena, 0.0, None, 0.0])
    return nombre_usuario

#PRE:
#POST: Da la bienvenida al usuario y solicita ingreso o registro, devuelve el nombre de usuario registrado/ingresado.
def menu_bienvenida()->str:
    print('⚽⚽⚽Bienvenido al sistema de apuestas e información deportiva del GRUPO 1⚽⚽⚽')
    opcion = ''
    while opcion != '0' and opcion != '1':
        opcion = input('Pulse 0 para ingresar a su cuenta o 1 para registrarse: ')
        if opcion != '0' and opcion != '1':
            print("Opción inválida. Intentá nuevamente.")
    if opcion == '0':
        nombre_usuario = ingreso_usuario()
    elif opcion == '1':
        nombre_usuario = registro_usuario()
    return nombre_usuario

#PRE:
#POST: Muestra las opciones disponibles, devuelve la opción elegida.
def menu(OPCIONES: tuple) -> str:
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("➡️  Listado de opciones ⬅️")
    opciones_validas = '123456789'
    for i in range(len(OPCIONES)):
        print(f'{i+1}- {OPCIONES[i]}')
    opcion = input('Elija una opción: ')
    while opcion not in opciones_validas:
        print('Opción incorrecta. Intente otra vez')
        for i in range(len(OPCIONES)):
            print(f'{i+1}- {OPCIONES[i]}')
        opcion = input('Elija una opción: ')
    return opcion

def main():
    OPCIONES = ('Mostrar plantel',
                'Mostrar tabla de posiciones',
                'Mostrar información de un equipo',
                'Grafico goles/minutos',
                'Cargar dinero',
                'Mostrar el usuario que mas dinero apostó',
                'Mostrar el usuario que mas veces ganó',
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
    ids_equipos = {'Gimnasia L.P.': 434,
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
               'Argentinos Jrs': 458,
               'Arsenal Sarandi': 459,
               'San Lorenzo': 460,
               'Sarmiento Junin': 474,
               'Instituto Cordoba': 478,
               'Platense': 1064,
               'Central Cordoba De Santiago': 1065,
               'Barracas Central': 2432}
    nombre_usuario = menu_bienvenida()
    opcion = menu(OPCIONES)
    while opcion != '9':
        os.system("cls")
        if opcion == '1':
            apuestas_e_informacion_deportiva.mostrar_jugadores(payload, HEADERS, ids_equipos)
        elif opcion =='2':
            apuestas_e_informacion_deportiva.mostrar_tabla_de_posiciones(HEADERS)
        elif opcion =='3':
            apuestas_e_informacion_deportiva.mostrar_escudo_e_informacion(payload, ids_equipos, HEADERS)
        elif opcion =='4':
            apuestas_e_informacion_deportiva.imprimir_grafico(ids_equipos, payload, HEADERS)
        elif opcion =='5':
            modificar_y_leer_archivoscsv.cargar_dinero(nombre_usuario)
        elif opcion =='6':
            modificar_y_leer_archivoscsv.usuario_mas_apostador()
        elif opcion =='7':
            modificar_y_leer_archivoscsv.usuario_mas_ganador()
        elif opcion =='8':
            dinero_disponible = modificar_y_leer_archivoscsv.obtener_dinero_disponible(nombre_usuario)
            if(dinero_disponible != 0):
                apuestas_e_informacion_deportiva.comenzar_sistema_apuestas(HEADERS, nombre_usuario, dinero_disponible)
            else:
                print("No tenes dinero disponible, hace una recarga.")
        opcion = menu(OPCIONES)
        os.system("cls")
main()