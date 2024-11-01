productos = []

opcion = 'in'

while opcion != '0':
    print("""
        Menu de ejemplo
        1. Carga datos
        2. Mostrar datos
        0. Salir""")

    opcion = input('Ingrese una opcion: ')

    if opcion == '1':
        print('carga de datos')
        nombre = input('Ingrese el nombre del producto: ')
        stock = int(input('Ingrese el stock del producto: '))
        
        nuevo_producto = [nombre, stock]
        productos.append(nuevo_producto)
    elif opcion == '2':
        print('muestra datos: ')
    elif opcion == '0':
        print('gracias por usar la App')