# Permitir a un usuario cargar dinero en su cuenta.
# Mostrar el usuario que más dinero apostó.
# Mostrar el usuario que más veces ganó.
import csv

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

def cargar_dinero(monto: int, nombre_usuario: str)->None:
    todos_los_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    for usuario in todos_los_usuarios:
        if usuario[1] == nombre_usuario:
            usuario[5] = float(usuario[5]) + monto
    with open("usuarios.csv", "w", newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow(["mail", "Nombre usuario", "Contrasenia", "Cantidad apostada hasta el momento", "Fecha ultima apuesta(YYYY/MM/DD)", "Dinero disponible"])
        escritor_csv.writerows(todos_los_usuarios)

def usuario_mas_apostador()->None:
    todos_los_usuarios = obtener_datos_de_los_usuarios("usuarios.csv")
    usuarios_y_montos = [[usuario[1],usuario[3]] for usuario in todos_los_usuarios]
    usuarios_y_montos.sort(key = lambda lista: float(lista[1]), reverse=True)
    
    print(f'El usuario que mas dinero aposto es {usuarios_y_montos[0][0]} con ${usuarios_y_montos[0][1]}')

def usuario_mas_ganador():
    pass
