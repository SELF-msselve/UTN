
#declaro la variable (lista) de productos y cantidades
#se inicializa con dos productos genericos
productos = [
    ['Manzanas', 5],
    ['Peras', 7]
]
#variable que levanta la opcion del menu
opcion = 'in'

#Funcion de carga de datos
def CargaDatos():
    print('carga de datos')
    #Se ingresan por variables separadas producto y cantidad
    nombre = input('Ingrese el nombre del producto: ')
    stock = int(input('Ingrese el stock del producto: '))
    #Se forma la dupla
    nuevo_producto = [nombre, stock]
    #Se agrega a la lista
    productos.append(nuevo_producto)   

#Funcion para imprimir la lista de productos.
def PrintProductos():
    for a in productos:
        print(f'Nombre Producto: {a[0]}, Cantidad: {a[1]}')
#El Bucle While del menu.
while opcion != '0':
    print("""
    Menu de ejemplo
        1. Carga datos
        2. Mostrar datos
        0. Salir""")

    opcion = input('Ingrese una opcion: ')
    #Se elige la opcion
    if opcion == '1':
        CargaDatos()
    elif opcion == '2':
        PrintProductos()
    elif opcion == '0':
        print('Gracias por usar la App')