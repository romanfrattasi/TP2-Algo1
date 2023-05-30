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
        nombre_usuario =input('El usuario que acabas de escribir no existe ')
    contrasena = input('Ingresa tu contraseña: ')
    contrasena=verificar_constrasenia(nombre_usuario,contrasena)
    print(contrasena)
    
def verificar_constrasenia(nombre_usuario,contrasenia):
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
                contrasenia=input("Error, esta no es la contrasenia correcta, intentelo otra vez")
            if  pbkdf2_sha256.verify(contrasenia, lista_contrasenias[i]):
                return contrasenia
                
                
                
                
                

            
    
    

    

def verificar_usuario_o_mail(usuario_o_mail, posicion_en_archivo, string):
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

def registro_usuario():
    email = input('Ingresa tu email: ')
    email = verificar_usuario_o_mail(email, 0, "email")  
    nombre_usuario = input('Ingresa tu nombre de usuario: ')
    nombre_usuario = verificar_usuario_o_mail(nombre_usuario, 1, "nombre de usuario")  

    
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