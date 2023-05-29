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

def registro_usuario():
    email = input('Ingresa tu email: ')
    nombre_usuario = input('Ingresa tu nombre de usuario: ')
    contrasena = input('Ingresa tu contraseña: ')
    hash_contrasena = pbkdf2_sha256.hash(contrasena)
    
    with open("usuarios.csv", 'a', newline='') as usuarios:
        escritor_csv = csv.writer(usuarios, delimiter=',')
        escritor_csv.writerow([email, nombre_usuario, hash_contrasena, 0.0, None, 0.0])
    menu.menu()

def main():
    menu_bienvenida()
main()


# from passlib.hash import pbkdf2_sha256
# contraseña = 'x'
# hash = pbkdf2_sha256.hash(contraseña)
# print(pbkdf2_sha256.verify('puto', hash))