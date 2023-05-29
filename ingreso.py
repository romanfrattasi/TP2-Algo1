import csv
from passlib.hash import pbkdf2_sha256
import menu

def menu_bienvenida():
    print('BIENVENIDO')
    opcion = ''
    while opcion != '0' and opcion != '1':
        opcion = input('Pulse 0 para ingresar a su cuenta o 1 para registrarse: ')
        if opcion != '0' and opcion != '1':
            print("Opción inválida. Intenta nuevamente.")
    if opcion == '0':
        ingreso_usuario()
    elif opcion == '1':
        registro_usuario()

def ingreso_usuario():
    nombre_usuario = input('Ingresa tu nombre de usuario: ')
    contrasena = input('Ingresa tu contraseña: ')
    
    
    

    
#para funcion ingresar usuario hay que comprobar
def verificar_usuario(usuario,mail):
    datos_usuario=[]
    with open("usuarios.csv", 'r', newline='') as usuarios:
        lista_usuario=[]
        lista_mail=[]
        datos = [usuario.splitlines() for usuario in usuarios][1:]
        for i in range(len(datos)):
            
            partes = datos[i][0].split(',')
            partes=partes[:2]
            datos_usuario.append(partes)
    for i in range(len(datos_usuario)):
        lista_usuario.append(datos_usuario[i][1])
        lista_mail.append(datos_usuario[i][0])
    while usuario in lista_usuario:
        usuario =input('Este nombre de usuario ya esta ocupado, escribe otro: ')
    while mail in lista_mail:
        mail=input('Este nmail ya esta ocupado, escribe otro ')    
    return usuario,mail
def registro_usuario():
    
    email = input('Ingresa tu email: ')
    nombre_usuario = input('Ingresa tu nombre de usuario: ')
    nombre_usuario,email=verificar_usuario(nombre_usuario,email)
    contrasena = input('Ingresa tu contraseña: ')
    hash_contrasena = pbkdf2_sha256.hash(contrasena)
    with open("usuarios.csv", 'a', newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow([email, nombre_usuario, hash_contrasena, 0.0, None, 0.0])
    menu.menu()
    
    
    

def main():
    lista_usuarios=[]
    lista_email=[]
    verificar_usuario(lista_usuarios,lista_email)
    menu_bienvenida()
main()


# from passlib.hash import pbkdf2_sha256
# contraseña = 'x'
# hash = pbkdf2_sha256.hash(contraseña)
# print(pbkdf2_sha256.verify('puto', hash))