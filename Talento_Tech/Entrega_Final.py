import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Crear un diccionario vacío
productos = {'Categoria': [], 'Producto': [], 'Stock': [], 'Precio': []}


def tab_1 ():
    
    # Función para cargar datos desde la base de datos SQLite al diccionario
    def load_from_db():
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
        
        cursor.execute('SELECT categoria, producto, stock, precio FROM productos')
        rows = cursor.fetchall()
        
        for row in rows:
            productos['Categoria'].append(row[0])
            productos['Producto'].append(row[1])
            productos['Stock'].append(row[2])
            productos['Precio'].append(row[3])
        
        conn.close()

    # Función para agregar un ítem al diccionario
    def add_item():
        categoria = category_var.get()
        producto = entry_product.get()
        stock = entry_stock.get()
        precio = entry_price.get()
        
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
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

    # Función para borrar el ítem seleccionado del diccionario
    def delete_item():
        try:
            selected_item_index = table.selection()[0]
            index = table.index(selected_item_index)
            del productos['Categoria'][index]
            del productos['Producto'][index]
            del productos['Stock'][index]
            del productos['Precio'][index]
            update_table()
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un ítem para borrar.")
    

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
        
        cursor.execute('DELETE FROM productos')  # Limpiar la tabla antes de insertar nuevos datos
        
        for i in range(len(productos["Producto"])):
            cursor.execute('''
                INSERT INTO productos (categoria, producto, stock, precio) VALUES (?, ?, ?, ?)
            ''', (productos["Categoria"][i], productos["Producto"][i], productos["Stock"][i], productos["Precio"][i]))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Información", "Datos guardados en la base de datos.")

    # Función para seleccionar un ítem de la tabla y mostrar sus valores en las entradas
    def select_item():
        
        button_update['state'] = 'normal'
        button_add['state'] = 'disable'
        button_delete['state'] = 'disable'
        button_save['state'] = 'disable'
        
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
        
        button_update['state'] = 'disable'
        button_add['state'] = 'normal'
        button_delete['state'] = 'normal'
        button_save['state'] = 'normal'
        
        try:
            selected_item_index = table.selection()[0]
            index = table.index(selected_item_index)
            
            categoria = category_var.get()
            producto = entry_product.get()
            stock = entry_stock.get()
            precio = entry_price.get()
            
            if categoria and producto and stock and precio:
                productos['Categoria'][index] = categoria
                productos['Producto'][index] = producto
                productos['Stock'][index] = stock
                productos['Precio'][index] = precio
                update_table()
                messagebox.showinfo("Información", "Ítem actualizado correctamente.")
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un ítem para actualizar.")

    # Función para actualizar la tabla con los datos del diccionario
    def update_table():
        for i in table.get_children():
            table.delete(i)
        for i in range(len(productos['Producto'])):
            table.insert("", "end", values=(productos['Categoria'][i], productos['Producto'][i], productos['Stock'][i], productos['Precio'][i]))
    
    
    # Crear y colocar el menú desplegable para la categoría
    category_var = tk.StringVar()
    category_var.set("Seleccionar categoría")
    categories = ["Frutas", "Verduras", "Tubérculos", "Hierbas", "Aromáticas", "Semillas"]

    label_category = ttk.Label(padre, text="Categoría:")
    label_category.grid(row=0, column=0, padx=10, pady=10)
    dropdown_category = ttk.OptionMenu(padre, category_var, *categories)
    dropdown_category.config(width=20)  # Ancho fijo del menú
    dropdown_category.grid(row=0, column=1, padx=10, pady=10)

    # Crear y colocar las etiquetas y entradas para producto, stock y precio
    label_product = ttk.Label(padre, text="Producto:")
    label_product.grid(row=1, column=0, padx=10, pady=10)
    entry_product = ttk.Entry(padre, width=30, justify="center")

    entry_product.grid(row=1, column=1, padx=10, pady=10)

    label_stock = ttk.Label(padre, text="Stock (Kg):")
    label_stock.grid(row=2, column=0, padx=10, pady=10)
    entry_stock = ttk.Entry(padre)
    entry_stock.grid(row=2, column=1, padx=10, pady=10)

    label_price = ttk.Label(padre, text="Precio ($):")
    label_price.grid(row=3, column=0, padx=10, pady=10)
    entry_price = ttk.Entry(padre)
    entry_price.grid(row=3, column=1, padx=10, pady=10)

    # Crear y colocar los botones para agregar, borrar, seleccionar y actualizar ítems
    button_add = ttk.Button(padre, text="Agregar", command=add_item)
    button_add.grid(row=0, column=2, pady=10)

    button_delete = ttk.Button(padre, text="Borrar", command=delete_item)
    button_delete.grid(row=1, column=2, pady=10)

    button_select = ttk.Button(padre, text="Seleccionar", command=select_item)
    button_select.grid(row=2, column=2, pady=10)

    button_update = ttk.Button(padre, text="Actualizar", command=update_item)
    button_update['state'] = 'disable'
    button_update.grid(row=3, column=2, pady=10)

    button_save = ttk.Button(padre, text="Guardar en DB", command=save_to_db)
    button_save.grid(row=6, columnspan=3, pady=10)

    # Crear y colocar la tabla para mostrar los ítems
    frame_table = ttk.Frame(padre)
    frame_table.grid(row=5, columnspan=3, padx=10, pady=10)

    table = ttk.Treeview(frame_table, columns=('Categoria', 'Producto', 'Stock', 'Precio'), show='headings')
    table.heading('Categoria', text='Categoria')
    table.heading('Producto', text='Producto')
    table.heading('Stock', text='Stock')
    table.heading('Precio', text='Precio')
    table.pack()

    # Cargar datos desde la base de datos al iniciar la aplicación
    load_from_db()
    update_table()


root = tk.Tk()
root.geometry('900x600')
root.title('Stock')

MainFrame = ttk.Frame(root)
MainFrame.pack()
MainTitle = ttk.Label(MainFrame, text='VERDULERIA RAMA VERDE')
MainTitle.pack()
SecondTitle = ttk.Label(MainFrame, text='Manejo de Stock')
SecondTitle.pack()

#notebook widget
notebook = ttk.Notebook(MainFrame)
notebook.pack(expand=True, fill='both')

padre = ttk.Frame(notebook,width=900, height=600)
tab2 = ttk.Frame(notebook,width=900, height=600)
padre.pack()
tab2.pack()

tab_1()


notebook.add(padre, text='Productos')
notebook.add(tab2, text='Reportes')


root.mainloop()