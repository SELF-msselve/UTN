import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Crear un diccionario vacío
data = {"Producto": [], "Stock": [], "Precio": []}

# Función para cargar datos desde la base de datos SQLite al diccionario
def load_from_db():
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            stock INTEGER,
            precio REAL
        )
    ''')
    
    cursor.execute('SELECT producto, stock, precio FROM productos')
    rows = cursor.fetchall()
    
    for row in rows:
        data["Producto"].append(row[0])
        data["Stock"].append(row[1])
        data["Precio"].append(row[2])
    
    conn.close()

# Función para agregar un ítem al diccionario
def add_item():
    product = entry_product.get()
    stock = entry_stock.get()
    price = entry_price.get()
    
    if product and stock and price:
        data["Producto"].append(product)
        data["Stock"].append(stock)
        data["Precio"].append(price)
        update_table()
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
        del data["Producto"][index]
        del data["Stock"][index]
        del data["Precio"][index]
        update_table()
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un ítem para borrar.")

# Función para actualizar la tabla con los datos del diccionario
def update_table():
    for i in table.get_children():
        table.delete(i)
    for i in range(len(data["Producto"])):
        table.insert("", "end", values=(data["Producto"][i], data["Stock"][i], data["Precio"][i]))

# Función para guardar el diccionario en una base de datos SQLite
def save_to_db():
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            stock INTEGER,
            precio REAL
        )
    ''')
    
    cursor.execute('DELETE FROM productos')  # Limpiar la tabla antes de insertar nuevos datos
    
    for i in range(len(data["Producto"])):
        cursor.execute('''
            INSERT INTO productos (producto, stock, precio) VALUES (?, ?, ?)
        ''', (data["Producto"][i], data["Stock"][i], data["Precio"][i]))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Información", "Datos guardados en la base de datos.")

# Crear la ventana principal
root = tk.Tk()
root.title("Lista de Productos")

# Crear y colocar las etiquetas y entradas para producto, stock y precio
label_product = tk.Label(root, text="Producto:")
label_product.grid(row=0, column=0, padx=10, pady=10)
entry_product = tk.Entry(root)
entry_product.grid(row=0, column=1, padx=10, pady=10)

label_stock = tk.Label(root, text="Stock:")
label_stock.grid(row=1, column=0, padx=10, pady=10)
entry_stock = tk.Entry(root)
entry_stock.grid(row=1, column=1, padx=10, pady=10)

label_price = tk.Label(root, text="Precio:")
label_price.grid(row=2, column=0, padx=10, pady=10)
entry_price = tk.Entry(root)
entry_price.grid(row=2, column=1, padx=10, pady=10)

# Crear y colocar los botones para agregar y borrar ítems
button_add = tk.Button(root, text="Agregar", command=add_item)
button_add.grid(row=3, column=0, pady=10)

button_delete = tk.Button(root, text="Borrar", command=delete_item)
button_delete.grid(row=3, column=1, pady=10)

button_save = tk.Button(root, text="Guardar en DB", command=save_to_db)
button_save.grid(row=5, columnspan=2, pady=10)

# Crear y colocar la tabla para mostrar los ítems
frame_table = tk.Frame(root)
frame_table.grid(row=4, columnspan=2, padx=10, pady=10)

table = ttk.Treeview(frame_table, columns=("Producto", "Stock", "Precio"), show="headings")
table.heading("Producto", text="Producto")
table.heading("Stock", text="Stock")
table.heading("Precio", text="Precio")
table.pack()

# Cargar datos desde la base de datos al iniciar la aplicación
load_from_db()
update_table()

# Ejecutar la aplicación
root.mainloop()
