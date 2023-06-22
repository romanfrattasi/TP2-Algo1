import csv
from datetime import datetime

#PRE:
#POST: Devuelve la fecha actual.
def obtener_fecha() -> str:
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime('%d-%m-%y')
    return fecha_formateada

#PRE: Recibe el monto a sumar, el nombre del usuario y la lista con todos los usuarios.
#POST: Actualiza el dinero disponible del usuario.
def cargar_dinero_a_csv_usuarios(monto: float, nombre_usuario: str, todos_los_usuarios: list) -> None:
    for usuario in todos_los_usuarios:
        if usuario[1] == nombre_usuario:
            usuario[5] = float(usuario[5]) + monto
    with open("usuarios.csv", "w", newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow(["mail", "Nombre usuario", "Contrasenia", "Cantidad apostada hasta el momento", "Fecha ultima apuesta(YYYY/MM/DD)", "Dinero disponible"])
        escritor_csv.writerows(todos_los_usuarios)

#PRE: Recibe el monto, el nombre y el tipo de transacción.
#POST: Agrega una transacción al archivo.
def cargar_a_csv_transacciones(monto: float, nombre_de_usuario: str, tipo_transaccion: str) -> None:
    fecha = obtener_fecha()
    with open("transacciones.csv", 'a', newline='') as transacciones:
        escritor_csv = csv.writer(transacciones, delimiter=',')
        escritor_csv.writerow([nombre_de_usuario, fecha, tipo_transaccion, monto])

#PRE: El archivo indicado no debe estar vacío.
#POST: Devuelve una lista con todos los datos de los usuarios presentes en el archivo.
def obtener_datos_de_los_usuarios(ruta_archivo:str) -> list:
    todos_los_usuarios=[]
    with open(ruta_archivo, 'r', newline='') as usuarios:
        datos_de_cada_usuario=[]
        datos = [usuario.splitlines() for usuario in usuarios][1:]
        for i in range(len(datos)):
            partes = datos[i][0].split(',')
            todos_los_usuarios.append(partes)
    for i in range(len(todos_los_usuarios)):
        datos_de_cada_usuario.append(todos_los_usuarios[i][1])
    return todos_los_usuarios

#PRE:
#POST: Devuelve el monto depositado por el usuario.
def pedir_monto_a_depositar() -> float:
    monto = None
    while monto is None:
        try :
            monto = float(input('Ingresá el monto que deseas depositar: '))
        except ValueError:
            print('El monto ingresado no es válido. Intentá de nuevo.')
    return monto

#PRE: Se recibe un nombre de usuario y el monto a depositar.
#POST: Actualiza el dinero disponible del usuario en el archivo.
def cargar_dinero(nombre_usuario: str)->None:
    monto = pedir_monto_a_depositar()
    usuarios_de_csv_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    cargar_dinero_a_csv_usuarios(monto, nombre_usuario , usuarios_de_csv_usuarios)
    cargar_a_csv_transacciones(monto, nombre_usuario, 'Deposita')
    print(f"Cargaste exitosamente en tu cuenta ${monto}.")

#PRE: Recibe el dinero disponible, el nombre del usuario y el dinero de la apuesta.
#POST: Actualiza en el archivo el dinero total apostado y la fecha de la última apuesta.
def cargar_datos_apuesta_a_csv_usuarios(dinero_disponible: float, nombre_usuario: str, dinero_apuesta: float) -> None:
    fecha = obtener_fecha()
    usuarios_csv_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    for usuario in usuarios_csv_usuarios:
        if usuario[1] == nombre_usuario:
            usuario[3] = float(usuario[3]) + dinero_apuesta
            usuario[4] = fecha
            usuario[5] =dinero_disponible
    with open("usuarios.csv", "w", newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow(["mail", "Nombre usuario", "Contrasenia", "Cantidad apostada hasta el momento", "Fecha ultima apuesta(YYYY/MM/DD)", "Dinero disponible"])
        escritor_csv.writerows(usuarios_csv_usuarios)

#PRE:
#POST: Muestra por pantalla el usuario que mas dinero apostó.
def usuario_mas_apostador()->None:
    todos_los_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    usuarios_y_montos = [[usuario[1],usuario[3]] for usuario in todos_los_usuarios]
    usuarios_y_montos.sort(key = lambda lista: float(lista[1]), reverse=True)
    print(f'🤑El usuario que mas dinero apostó es {usuarios_y_montos[0][0]} con ${usuarios_y_montos[0][1]}🤑')

#PRE: Recibe un nombre de usuario y una lista con todos los usuarios.
#POST: Devuelve la lista específica del usuario seleccionado.
def filtrar_usuarios(nombre_usuario: str, todos_los_usuarios: list) -> list:
    for usuario in todos_los_usuarios:
        if usuario[1] == nombre_usuario:
            return usuario

#PRE: Recibe un nombre de usuario.
#POST: Devuelve el dinero que tiene disponible dicho usuario
def obtener_dinero_disponible(nombre_usuario: str) -> float:
    todos_los_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    usuario = filtrar_usuarios(nombre_usuario, todos_los_usuarios)
    dinero_disponible = float(usuario[5])
    return dinero_disponible

#PRE:
#POST: Imprime por pantalla el usuario que mas veces ganó.
def usuario_mas_ganador() -> None:
    lista_usuarios=obtener_datos_de_los_usuarios("transacciones.csv")
    diccionario_ganador={}
    for usuario in lista_usuarios:
        if usuario[0] not in diccionario_ganador:
            diccionario_ganador[usuario[0]]=0
            if usuario[2]=="Gana":
                diccionario_ganador[usuario[0]]=1
        else:
            if usuario[2]=="Gana":
                diccionario_ganador[usuario[0]]+=1
    usuario_mas_ganador=(sorted(diccionario_ganador.items(),key=lambda x:x[1],reverse=True)[:1])
    print(f"💸El usuario mas ganador es {usuario_mas_ganador[0][0]} con una tolidad de {usuario_mas_ganador[0][1]} victorias💸")