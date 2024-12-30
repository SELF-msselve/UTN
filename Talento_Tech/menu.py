import tkinter as tk   
import pandas as pd
from tkinter import * 
from tkinter import filedialog as fd
from tkinter import ttk
import os
import clase_db as db


def funcion_include(nombre_tabla):
    data = {
        'Columna1': range(1, 11),
        'Columna2': [f'{nombre_tabla} {i}' for i in range(1, 11)],
        'Columna3': [i * 10 for i in range(1, 11)]
    }
    nombre = 'Poti-' + nombre_tabla
    df = pd.DataFrame(data)
    dataBase.save_to_db(nombre, df)
    update_table_2() 

def new_proyect():
    global dbFilePath
    dbFilePath = fd.asksaveasfilename(title='New Proyect...',
                initialfile = 'Untitled.db',
                defaultextension=".db",filetypes=[("All Files","*.*"),("Data Base","*.db")])
    global dataBase
    dataBase = db.data_base(dbFilePath)
    data = {
            'Columna1': False
    }
    nombre = 'index'
    df = pd.DataFrame(data)
    dataBase.save_to_db(nombre, df)
    update_table_2() 

def open_proyect():
    filetypes = (('Proyect', '*.db'), ('Files', '*.db'))

    dbFilePath = fd.askopenfilename(
        title='Open Proyect...',
        initialdir='/',
        filetypes=filetypes)
    
    global dataBase
    dataBase = db.data_base(dbFilePath)
    print(dataBase.list_tables())
    update_table_2()

def update_table_2():
    for i in table_2.get_children():
        table_2.delete(i)
#    for i in range(len(filter_table['Producto'])):
#        table_2.insert("", "end", values=(filter_table['Categoria'][i], filter_table['Producto'][i], filter_table['Stock'][i], filter_table['Precio'][i]))
    df = dataBase.list_tables()
    for i, row in df.iterrows(): 
        table_2.insert("", "end", values=list(row)) 

def show_selected(event):
    selected_item = table_2.selection()
    if selected_item:
        item = table_2.item(selected_item)
        values = item['values']
        selected_label.config(text=f'Selected: {values}')


root = tk.Tk()
root.title('Hola Mundo')
root.geometry("400x200")

menuBar = Menu(root)
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label='New Proyect', command=lambda: new_proyect())
fileMenu.add_command(label='Open Proyect', command=lambda: open_proyect())
menuBar.add_cascade(label='File', menu= fileMenu)

root.config(menu = menuBar) #menu(main_frame))

mainFrame = tk.Frame(root)
mainFrame.pack()

boton1 = tk.Button(mainFrame, text='Poti', command=lambda: funcion_include('tabla20'))
boton1.pack()
boton2 = tk.Button(mainFrame, text='Update', command=lambda: update_table_2())
boton2.pack()

selected_label = tk.Label(mainFrame, text="Selecciona un item") 
selected_label.pack()



table_2 = ttk.Treeview(root, columns=('Poti'), show='headings')
table_2.heading('Poti', text='Poti')
table_2.column('Poti', width=100) 
table_2.bind("<<TreeviewSelect>>", show_selected)
table_2.pack(fill="both", expand=True)

root.mainloop()

