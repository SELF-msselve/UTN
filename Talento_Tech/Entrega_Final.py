# Se importan las librerias necesarias.
# tkinter, libreria de ventanas y widgets
import tkinter as tk
from tkinter import ttk, messagebox
# Manejo de base de datos.
import sqlite3

# --------------PROFE-----------------
# Muchas Gracias por el excelente curso.
# Pido disculpas si en algun momento fui insistente o grosero pidiendo de avanzar y no dispersarse en conversaciones laterales.
# Lo que sucede es que considero que al ser un curso gratuito la gente debe entender que hay que sacar el maximo provecho.
# Para distenderse o conversar pueden usar otros medios.

# Por mi lado te agradezco infinitamente tu predisposicion y EXCELENTE didactica al transmitir.
# Me motivo a avanzar un poco mas alla. 

# Verdaderamente, me ayude mucho con chatGPT y Copilot. Pero me motivo el sentido que le dieron Uds. al curso.
# Espero poder participar de las ediciones que siguen.
# Tambien que realicen un curso Intermedio y uno avanzado de Python.
# Me gustaria aprender bien de tus conocimientos sobre Clases. 
# Muchas Gracias por todo.

# --------Paso a Comentar la App-----------

# La App tiene dos Tab, como los de Excel.
# Un Tab para trabajar con los Datos.
#   Ingresar Datos.
#   Borrar Datos seleccionando la fila.
#   Editar Datos. Seleccionando la fila y Actualizando.

# Un Tab para generar consultas.
#   Filtrar por Categoria.
#   Filtrar por un Stock minimo ingresado por el usuario.

# ----------Aqui el codigo------------------

# Crear un diccionario vacío. Se utiliza, por si no existe una base de datos
productos = {'Categoria': [], 'Producto': [], 'Stock': [], 'Precio': []}
# Crear un nuevo diccionario vacío para los resultados filtrados
categoria_filtrada = {'Categoria': [], 'Producto': [], 'Stock': [], 'Precio': []}

# Función para cargar datos desde la base de datos SQLite al diccionario de la App.
def load_from_db():
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()

# Si la Table y la Base de Datos no Existe la Crea.
# El usuario no puede cambiar el nombre.
# Eso quedara para otro curso, jejejeje.    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            producto TEXT,
            stock INTEGER,
            precio REAL
        )
    ''')
    
    cursor.execute('SELECT categoria, producto, stock, precio FROM productos')
    rows = cursor.fetchall()
    
    for row in rows:
        productos['Categoria'].append(row[0])
        productos['Producto'].append(row[1])
        productos['Stock'].append(row[2])
        productos['Precio'].append(row[3])
    
    conn.close()

# Función para guardar el diccionario en una base de datos SQLite
def save_to_db():
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            producto TEXT,
            stock INTEGER,
            precio REAL
        )
    ''')
    # Limpiar la tabla antes de insertar nuevos datos
    cursor.execute('DELETE FROM productos')
    # Recorre el diccionario para guardarlo en la Base de Datos.
    for i in range(len(productos["Producto"])):
        cursor.execute('''
            INSERT INTO productos (categoria, producto, stock, precio) VALUES (?, ?, ?, ?)
        ''', (productos["Categoria"][i], productos["Producto"][i], productos["Stock"][i], productos["Precio"][i]))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Información", "Datos guardados en la base de datos.")


# Llama a la Funcion Cargar datos desde la base de datos al iniciar la aplicación
load_from_db()

# Esta es la funcion del Tab donde se trabaja con los Datos
def tab_1 ():
    # Función para agregar un ítem al diccionario
    def add_item():
        # Se levanta los datos de las celdas de Entrada
        categoria = category_var.get()
        producto = entry_product.get()
        stock = int(entry_stock.get())
        precio = float(entry_price.get())
        # Verifica que esten todos los datos para agregr al dicc.
        if categoria and producto and stock and precio:
            productos['Categoria'].append(categoria)
            productos['Producto'].append(producto)
            productos['Stock'].append(stock)
            productos['Precio'].append(precio)
            update_table()
            category_var.set("Seleccionar categoría")
            entry_product.delete(0, tk.END)
            entry_stock.delete(0, tk.END)
            entry_price.delete(0, tk.END)
        # Si no estan todos los datos da un msg.
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

    # Función para borrar el ítem seleccionado del diccionario
    def delete_item():
        try:
            # Toma el indice del diccionaro de la seleccion del usuario.
            # Es increible, hay una funcion de tkinter que ve que selecciono el usuario.
            selected_item_index = table.selection()[0]
            index = table.index(selected_item_index)
            del productos['Categoria'][index]
            del productos['Producto'][index]
            del productos['Stock'][index]
            del productos['Precio'][index]
            #Actualiza la tabla sin los nuevos datos.
            update_table()
        except IndexError:
            # Si el usuario no selecciono un item, da un msg.
            messagebox.showwarning("Advertencia", "Por favor, seleccione un ítem para borrar.")

    # Función para seleccionar un ítem de la tabla y mostrar sus valores en las entradas
    def select_item():
        # Cuando el Usuario Pide cambiar un dato y lo selecciona.
        # Se desactivan todos los botones excepto el de Actualizar.
        button_update['state'] = 'normal' # solo este boton queda activo
        button_add['state'] = 'disable'
        button_delete['state'] = 'disable'
        button_save['state'] = 'disable'
        # Aca se cargan los valores en las celdas Entry.
        try:
            selected_item_index = table.selection()[0]
            index = table.index(selected_item_index)
            
            category_var.set(productos['Categoria'][index])
            entry_product.delete(0, tk.END)
            entry_stock.delete(0, tk.END)
            entry_price.delete(0, tk.END)
            
            entry_product.insert(0, productos['Producto'][index])
            entry_stock.insert(0, productos['Stock'][index])
            entry_price.insert(0, productos['Precio'][index])
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un ítem de la tabla.")

    # Función para actualizar un ítem seleccionado en el diccionario
    def update_item():
        # Una vez que se presiona el boton Update.
        button_update['state'] = 'disable'  # Se desactiva este boton
        # Y se activan todos los demas.
        button_add['state'] = 'normal'
        button_delete['state'] = 'normal'
        button_save['state'] = 'normal'
        # Se actualizan los datos en el Diccionario.
        try:
            selected_item_index = table.selection()[0]
            index = table.index(selected_item_index)
            
            categoria = category_var.get()
            producto = entry_product.get()
            stock = entry_stock.get()
            precio = entry_price.get()
            # Verifica que esten todos los datos ingresados. Caso contrario emite un msg.
            if categoria and producto and stock and precio:
                productos['Categoria'][index] = categoria
                productos['Producto'][index] = producto
                productos['Stock'][index] = int(stock)
                productos['Precio'][index] = float(precio)
                update_table()
                category_var.set("Seleccionar categoría")
                entry_product.delete(0, tk.END)
                entry_stock.delete(0, tk.END)
                entry_price.delete(0, tk.END)
                messagebox.showinfo("Información", "Ítem actualizado correctamente.")
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un ítem para actualizar.")

    # Función para actualizar la tabla con los datos del diccionario
    def update_table():
        # Primero se borra toda la tabla.
        for i in table.get_children():
            table.delete(i)
        # Se actualiza la tabla con los datos del diccionario.
        for i in range(len(productos['Producto'])):
            table.insert("", "end", values=(productos['Categoria'][i], productos['Producto'][i], productos['Stock'][i], productos['Precio'][i]))

# Aca comienza la parte Grafica del Tab 1.
# Se dibujan las Etiquetas, celdas de entrada y Botones.
# Las explico aca, pero todo se repite a lo largo de la App.
    # Etiqueta solo para Escribir un texto en pantalla
    label_category = ttk.Label(tab1, text='Categoría:')
    # Se coloca dentro de una grilla y se le da una separacion de otros objetos
    label_category.grid(row=0, column=0, padx=10, pady=10)
    # Este es un menu desplegable. El usuario elige la categoria.
    # La eleccion se guarda en category_var
    dropdown_category = ttk.OptionMenu(tab1, category_var, *categories)
    dropdown_category.config(width=30)  # Ancho fijo del menú
    dropdown_category.grid(row=0, column=1, padx=10, pady=10)

    # Crear y colocar las etiquetas y entradas para producto, stock y precio
    label_product = ttk.Label(tab1, text="Producto:")
    label_product.grid(row=1, column=0, padx=10, pady=10)
    # Esta es una celda para ingresar texto.
    entry_product = ttk.Entry(tab1, width=30, justify="center")
    entry_product.grid(row=1, column=1, padx=10, pady=10)

    label_stock = ttk.Label(tab1, text="Stock (Kg):")
    label_stock.grid(row=2, column=0, padx=10, pady=10)
    entry_stock = ttk.Entry(tab1, width=30, justify="center")
    entry_stock.grid(row=2, column=1, padx=10, pady=10)

    label_price = ttk.Label(tab1, text="Precio ($):")
    label_price.grid(row=3, column=0, padx=10, pady=10)
    entry_price = ttk.Entry(tab1, width=30, justify="center")
    entry_price.grid(row=3, column=1, padx=10, pady=10)

    # Crear y colocar los botones para agregar, borrar, seleccionar y actualizar ítems
    # el boton tiene adentro la opcion de llamar a una funcion al ser presionado.
    button_add = ttk.Button(tab1, text="Agregar Producto", command=add_item, width=30)
    button_add.grid(row=0, column=2, pady=10)

    button_delete = ttk.Button(tab1, text="Borrar Producto", command=delete_item, width=30)
    button_delete.grid(row=1, column=2, pady=10)

    button_select = ttk.Button(tab1, text="Modificar Producto", command=select_item, width=30)
    button_select.grid(row=2, column=2, pady=10)

    button_update = ttk.Button(tab1, text="Actualizar", command=update_item, width=30)
    # Este boton que llama a la funcion de Actualizacion de un dato aparece desactivado.
    # solo se activa cuando el usuario elije la opcion "Modificar Producto"
    button_update['state'] = 'disable'
    button_update.grid(row=3, column=2, pady=10)

    button_save = ttk.Button(tab1, text="Guardar en DB", command=save_to_db, width=30)
    button_save.grid(row=6, columnspan=3, pady=10)

    # Crear y colocar la tabla para mostrar los ítems
    frame_table = ttk.Frame(tab1)
    frame_table.grid(row=5, columnspan=3, padx=10, pady=10)

    # Esta tabla se crea con los mismos encabesados del diccionario.
    # La tabla se actualiza con una funcion, mencionada mas arriba.
    table = ttk.Treeview(frame_table, columns=('Categoria', 'Producto', 'Stock', 'Precio'), show='headings')
    # Se definen los encabezados
    table.heading('Categoria', text='Categoria', anchor="center")
    table.heading('Producto', text='Producto')
    table.heading('Stock', text='Stock')
    table.heading('Precio', text='Precio')
    # Se definen las columnas con los valores centrados.
    table.column('Categoria', anchor='center')
    table.column('Producto', anchor='center')
    table.column('Stock', anchor='center')
    table.column('Precio', anchor='center')
    table.pack()
    # Se llama a la funcion para actualizar la tabla mencionada.
    update_table()

# Esta es la funcion del Tab donde se trabaja con los filtros del diccionario
def tab_2 ():
    # Funcion para limpiar el Diccionario Filtro.
    def limpia_diccionario_filtro():
        categoria_filtrada['Categoria'].clear()
        categoria_filtrada['Producto'].clear()
        categoria_filtrada['Stock'].clear()
        categoria_filtrada['Precio'].clear()        
    # funcion para generar un nuevo diccionario con el filtro de categoria.
    # el usuario selecciona una categoria de la lista.
    
    # funcion para Filtrar por Categoria
    def filter_category():
        categoria = category_var.get()

        limpia_diccionario_filtro()
        
        # Recorrer el diccionario original
        for i in range(len(productos['Categoria'])):
            if productos['Categoria'][i] == categoria:
                # Agregar los elementos que coinciden con la categoría al nuevo diccionario
                categoria_filtrada['Categoria'].append(productos['Categoria'][i])
                categoria_filtrada['Producto'].append(productos['Producto'][i])
                categoria_filtrada['Stock'].append(productos['Stock'][i])
                categoria_filtrada['Precio'].append(productos['Precio'][i])
        update_table_2(categoria_filtrada)

    # funcion para Filtrar por Stock minimo ingresado por el usuario
    def filter_stock_min():
        stock_min = int(entry_stock_min.get())
        
        limpia_diccionario_filtro()
        # Recorrer el diccionario original
        for i in range(len(productos['Categoria'])):
            if productos['Stock'][i] <= stock_min:
                # Agregar los elementos que coinciden con la categoría al nuevo diccionario
                categoria_filtrada['Categoria'].append(productos['Categoria'][i])
                categoria_filtrada['Producto'].append(productos['Producto'][i])
                categoria_filtrada['Stock'].append(productos['Stock'][i])
                categoria_filtrada['Precio'].append(productos['Precio'][i])
        # Aca si el filtro no da un resultado, avisa que no hay datos filtrados.
        if all(len(v) == 0 for v in categoria_filtrada.values()):
            messagebox.showinfo('Filtro Stock Minimo', f'No existen Productos con stock menor a {stock_min}')

        update_table_2(categoria_filtrada)        
    
    # Idem a update table.
    def update_table_2(filter_table):
        for i in table_2.get_children():
            table_2.delete(i)
        for i in range(len(filter_table['Producto'])):
            table_2.insert("", "end", values=(filter_table['Categoria'][i], filter_table['Producto'][i], filter_table['Stock'][i], filter_table['Precio'][i]))

    # en esta seccion se construye todas las vistas del TAB_2. Etiquetas, Entradas y botones. Idem TAB_1  
    label_category = ttk.Label(tab2, text='Seleccione una Categoría para Filtrar')
    label_category.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    dropdown_category = ttk.OptionMenu(tab2, category_var, *categories)
    dropdown_category.config(width=30)  # Ancho fijo del menú
    dropdown_category.grid(row=0, column=1, padx=10, pady=10)
    
    button_filter = ttk.Button(tab2, text="Filtrar", command=filter_category, width=30)
    button_filter.grid(row=0, column=2, padx=10, pady=10, sticky='e')   

      
    label_stock = ttk.Label(tab2, text='Ingrese el Stock Minimo para Filtrar (<=)')
    label_stock.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    entry_stock_min = ttk.Entry(tab2, width=30, justify="center")
    entry_stock_min.grid(row=1, column=1, padx=10, pady=10)
    
    button_stock = ttk.Button(tab2, text="Filtrar", command=filter_stock_min, width=30)
    button_stock.grid(row=1, column=2, padx=10, pady=10, sticky='e')   

    # Crear y colocar la tabla para mostrar los ítems FILTRADOS
    frame_table_2 = ttk.Frame(tab2)
    frame_table_2.grid(row=2, columnspan=3, padx=10, pady=10)

    table_2 = ttk.Treeview(frame_table_2, columns=('Categoria', 'Producto', 'Stock', 'Precio'), show='headings')
    table_2.heading('Categoria', text='Categoria')
    table_2.heading('Producto', text='Producto')
    table_2.heading('Stock', text='Stock')
    table_2.heading('Precio', text='Precio')
    # Se definen las columnas
    table_2.column('Categoria', anchor='center')
    table_2.column('Producto', anchor='center')
    table_2.column('Stock', anchor='center')
    table_2.column('Precio', anchor='center')
    table_2.pack(side="left", fill="both", expand=True)


# Esta es la seccion principal, donde se genera la Ventana Principal.
# Esta es el padre de todas las otras ventanas.
root = tk.Tk()
# Ancho y alto de la ventana.
root.geometry('825x550')
# el usuario no la puede ajustar. solo la puede mover.
#root.resizable(False, False)
# Titulo de la Ventana.
root.title('Stock Rama Verde')

# Crear y colocar el menú desplegable para la categoría
category_var = tk.StringVar()
#category_var.set(). son las categorias de productos. El usuario no los puede modificar.
categories = ['Seleccionar categoría', 'Fruta', 'Verdura', 'Tubérculo', 'Hierbas', 'Aromáticas', 'Semillas', 'Granja', 'Cereal']

# PArecido a html se pueden crear estilos para ttk.
style = ttk.Style()
style.configure('TLabel_1.TLabel', font=('Helvetica', 16))
style.configure('TLabel_2.TLabel', font=('Arial', 11))

# Se crea un Frame que va a albergar los widgets dentro de la ventana padre root.
MainFrame = ttk.Frame(root)
# Siempre se debe hacer un pack o hubicar dentro de cada Frame.
MainFrame.pack()
MainTitle = ttk.Label(MainFrame, text='VERDULERIA RAMA VERDE', style='TLabel_1.TLabel')
MainTitle.pack()
SecondTitle = ttk.Label(MainFrame, text='Manejo de Stock', style='TLabel_2.TLabel')
SecondTitle.pack()

# Aca se crea el notebook widget. son como los tabs de excel.
notebook = ttk.Notebook(MainFrame)
notebook.pack(expand=True, fill='both')
# Se crean las variables tipo frame que se van a albergar dentro del notebook. En este caso son solo 2 pero se pueden poner mas.
tab1 = ttk.Frame(notebook,width=825, height=550)
tab2 = ttk.Frame(notebook,width=825, height=550)
tab1.pack()
tab2.pack()

# Para simplificar y ordenar el codigo cree dos funciones mas arriba que son los tabs.
# Aca se llaman a esas funciones.
tab_1()
tab_2()

# Se agregan las variables al notebook.
notebook.add(tab1, text='   Productos   ')
notebook.add(tab2, text='   Reportes   ')

# Esto hace que la ventna pricipal y todos sus hijos permanezcan activas y atentas a las acciones del usuario.
# Es un loop permanente de la App para mantener todo funcionando.
root.mainloop()