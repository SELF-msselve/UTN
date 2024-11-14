productos = [
    ['Manzanas', 5],
    ['Peras', 7]
]

opcion = 'in'

def CargaDatos():
    print('carga de datos')
    nombre = input('Ingrese el nombre del producto: ')
    stock = int(input('Ingrese el stock del producto: '))
    
    nuevo_producto = [nombre, stock]
    productos.append(nuevo_producto)   

def PrintProductos():
    for a in productos:
        print(f'Nombre Producto: {a[0]}, Cantidad: {a[1]}')

while opcion != '0':
    print("""
    Menu de ejemplo
        1. Carga datos
        2. Mostrar datos
        0. Salir""")

    opcion = input('Ingrese una opcion: ')

    if opcion == '1':
        CargaDatos()
    elif opcion == '2':
        PrintProductos()
    elif opcion == '0':
        print('Gracias por usar la App')