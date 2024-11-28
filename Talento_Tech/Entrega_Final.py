import tkinter as tk 
from tkinter import ttk, messagebox 
import pandas as pd


# Crear un DataFrame vacío
df = pd.DataFrame(columns=["Producto", "Stock", "Precio"])

root = tk.Tk()
root.geometry('600x400')
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

tab1 = ttk.Frame(notebook,width=600, height=200)
tab2 = ttk.Frame(notebook,width=600, height=200)
tab1.pack()
tab2.pack()

# Función para agregar un ítem a la lista
def add_item():
    product = entry_product.get()
    stock = entry_stock.get()
    price = entry_price.get()
    
    if product and stock and price:
        listbox.insert(tk.END, f"Producto: {product}, Stock: {stock}, Precio: {price}")
        entry_product.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        pass
        # tk.messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")


# Crear y colocar las etiquetas y entradas para producto, stock y precio
label_product = tk.Label(tab1, text="Producto:")
label_product.grid(row=0, column=0, padx=10, pady=10)
entry_product = tk.Entry(tab1)
entry_product.grid(row=0, column=1, padx=10, pady=10)

label_stock = tk.Label(tab1, text="Stock:")
label_stock.grid(row=1, column=0, padx=10, pady=10)
entry_stock = tk.Entry(tab1)
entry_stock.grid(row=1, column=1, padx=10, pady=10)

label_price = tk.Label(tab1, text="Precio:")
label_price.grid(row=2, column=0, padx=10, pady=10)
entry_price = tk.Entry(tab1)
entry_price.grid(row=2, column=1, padx=10, pady=10)

# Crear y colocar el botón para agregar ítems
button_add = tk.Button(tab1, text="Agregar", command=add_item)
button_add.grid(row=3, columnspan=2, pady=10)

# Crear y colocar el listbox para mostrar los ítems
listbox = tk.Listbox(tab1, width=50)
listbox.grid(row=4, columnspan=2, padx=10, pady=10)


notebook.add(tab1, text='Egregar Producto')
notebook.add(tab2, text='Eliminar Producto')


root.mainloop()