import ingreso, buscar_usuarios

def menu():
    nombre_usuario = ingreso.menu_bienvenida()
    OPCIONES = ('Mostrar plantel',
                'Mostrar tabla de posiciones',
                'Mostrar informacion de un equipo',
                'Grafico goles/minutos',
                'Cargar dinero',
                'Mostrar el usuario que mas dinero aposto',
                'Mostrar el usuario que mas veces gano',
                'Salir'
                )
    
    for i in range(len(OPCIONES)):
        print(f'{i+1}- {OPCIONES[i]}')
    opcion = input('Elija una opcion: ')
    
    while opcion != '8':
        if opcion == '1':
            pass
        elif opcion =='2':
            pass
        elif opcion =='3':
            pass
        elif opcion =='4':
            pass
        elif opcion =='5':
            numero = None
            while numero is None:
                try :
                    numero = float(input('Ingresa el monto que deseas depositar: '))
                except ValueError:
                    print('El monto ingresado no es valido. Intenta de nuevo.')
            buscar_usuarios.cargar_dinero(numero, nombre_usuario)
        elif opcion =='6':
            pass
        elif opcion =='7':
            pass
        else:
            print('Opcion incorrecta. Intente otra vez')
        OPCIONES = ('Mostrar plantel',
                'Mostrar tabla de posiciones',
                'Mostrar informacion de un equipo',
                'Grafico goles/minutos',
                'Cargar dinero',
                'Mostrar el usuario que mas dinero aposto',
                'Mostrar el usuario que mas veces gano',
                'Salir'
                )
        for i in range(len(OPCIONES)):
            print(f'{i+1}- {OPCIONES[i]}')
        opcion = input('Elija una opcion: ')
    

def main():
    menu()
main()