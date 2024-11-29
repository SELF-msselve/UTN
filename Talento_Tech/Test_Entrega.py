import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Crear un diccionario vacío
productos = {'Categoria': [], 'Producto': [], 'Stock': [], 'Precio': []}

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
    categoria = entry_category.get()
    producto = entry_product.get()
    stock = entry_stock.get()
    precio = entry_price.get()
    
    if categoria and producto and stock and precio:
        productos['Categoria'].append(categoria)
        productos['Producto'].append(producto)
        productos['Stock'].append(stock)
        productos['Precio'].append(precio)
        update_table()
        entry_category.delete(0, tk.END)
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

# Función para actualizar la tabla con los datos del diccionario
def update_table():
    for i in table.get_children():
        table.delete(i)
    for i in range(len(productos['Producto'])):
        table.insert("", "end", values=(productos['Categoria'][i], productos['Producto'][i], productos['Stock'][i], productos['Precio'][i]))

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
            INSERT INTO productos (producto, stock, precio) VALUES (?, ?, ?)
        ''', (productos["Categoria"][i], productos["Producto"][i], productos["Stock"][i], productos["Precio"][i]))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Información", "Datos guardados en la base de datos.")

# Crear la ventana principal
root = tk.Tk()
root.title("Lista de Productos")

# Crear y colocar las etiquetas y entradas para producto, stock y precio
label_category = tk.Label(root, text="Categoria:")
label_category.grid(row=0, column=1, padx=10, pady=10)
entry_category = tk.Entry(root)
entry_category.grid(row=0, column=2, padx=10, pady=10)

label_product = tk.Label(root, text="Producto:")
label_product.grid(row=1, column=1, padx=10, pady=10)
entry_product = tk.Entry(root)
entry_product.grid(row=1, column=2, padx=10, pady=10)

label_stock = tk.Label(root, text="Stock (Kg):")
label_stock.grid(row=2, column=1, padx=10, pady=10)
entry_stock = tk.Entry(root)
entry_stock.grid(row=2, column=2, padx=10, pady=10)

label_price = tk.Label(root, text="Precio ($):")
label_price.grid(row=3, column=1, padx=10, pady=10)
entry_price = tk.Entry(root)
entry_price.grid(row=3, column=2, padx=10, pady=10)

# Crear y colocar los botones para agregar y borrar ítems
button_add = tk.Button(root, text="Agregar", command=add_item)
button_add.grid(row=0, column=0, pady=10)

button_delete = tk.Button(root, text="Borrar", command=delete_item)
button_delete.grid(row=1, column=0, pady=10)

button_save = tk.Button(root, text="Guardar en DB", command=save_to_db)
button_save.grid(row=6, columnspan=3, pady=10)

# Crear y colocar la tabla para mostrar los ítems
frame_table = tk.Frame(root)
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

# Ejecutar la aplicación
root.mainloop()
