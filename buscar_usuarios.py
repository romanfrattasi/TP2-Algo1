import csv
from datetime import datetime

def obtener_fecha():
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime('%d-%m-%y')
    
    return fecha_formateada

def cargar_dinero_a_csv_usuarios(monto, nombre_usuario , todos_los_usuarios):
    for usuario in todos_los_usuarios:
        if usuario[1] == nombre_usuario:
            usuario[5] = float(usuario[5]) + monto
    with open("usuarios.csv", "w", newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow(["mail", "Nombre usuario", "Contrasenia", "Cantidad apostada hasta el momento", "Fecha ultima apuesta(YYYY/MM/DD)", "Dinero disponible"])
        escritor_csv.writerows(todos_los_usuarios)
        
def cargar_a_csv_transacciones(monto, nombre_de_usuario, tipo_transaccion):
    fecha = obtener_fecha()
    with open("transacciones.csv", 'a', newline='') as transacciones:
        escritor_csv = csv.writer(transacciones, delimiter=',')
        escritor_csv.writerow([nombre_de_usuario, fecha, tipo_transaccion, monto])

#PRE: El archivo indicado no debe estar vacío.
#POST: Devuelve una lista con todos los datos de los usuarios presentes en el archivo.
def obtener_datos_de_los_usuarios(ruta_archivo:str)->list:
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

#PRE: Se recibe un nombre de usuario y el monto a depositar.
#POST: Actualiza el dinero disponible del usuario en el archivo.
def cargar_dinero(monto: float, nombre_usuario: str)->None:
    usuarios_de_csv_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    cargar_dinero_a_csv_usuarios(monto, nombre_usuario , usuarios_de_csv_usuarios)
    cargar_a_csv_transacciones(monto, nombre_usuario, 'Deposita')
    
def cargar_datos_apuesta_a_csv_usuarios(dinero_disponible, nombre_usuario, dinero_apuesta):
    fecha = obtener_fecha()
    usuarios_csv_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    for usuario in usuarios_csv_usuarios:
        if usuario[1] == nombre_usuario:
            usuario[3] = float(usuario[3]) + dinero_apuesta
            usuario[4] = fecha
            usuario[5] = float(usuario[5]) + dinero_disponible
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
    
    print(f'El usuario que mas dinero aposto es {usuarios_y_montos[0][0]} con ${usuarios_y_montos[0][1]}')

#PRE:
#POST:

def filtrar_usuarios(nombre_usuario, todos_los_usuarios):
    for usuario in todos_los_usuarios:
        if usuario[1] == nombre_usuario:
            return usuario

def obtener_dinero_disponible(nombre_usuario):
    todos_los_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    usuario = filtrar_usuarios(nombre_usuario, todos_los_usuarios)
    dinero_disponible = float(usuario[5])
    
    return dinero_disponible

def usuario_mas_ganador():
    pass
