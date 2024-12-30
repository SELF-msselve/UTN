import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import os

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Management")

        # Crear el menú principal
        menubar = tk.Menu(root)
        
        # Crear el sub-menú "Base de Datos"
        database_menu = tk.Menu(menubar, tearoff=0)
        database_menu.add_command(label="Crear Base de Datos", command=self.create_database)
        database_menu.add_command(label="Abrir Base de Datos", command=self.open_database)
        
        menubar.add_cascade(label="Base de Datos", menu=database_menu)
        root.config(menu=menubar)
        
        self.db_name = None

    def create_database(self):
        """ Crear una nueva base de datos con el nombre proporcionado por el usuario """
        db_name = simpledialog.askstring("Crear Base de Datos", "Ingrese el nombre de la base de datos:")
        if db_name:
            if not db_name.endswith('.db'):
                db_name += '.db'
            try:
                conn = sqlite3.connect(db_name)
                conn.close()
                messagebox.showinfo("Éxito", f"Base de datos '{db_name}' creada exitosamente.")
                self.db_name = db_name
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al crear la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "El nombre de la base de datos no puede estar vacío.")

    def open_database(self):
        """ Abrir una base de datos existente """
        db_name = simpledialog.askstring("Abrir Base de Datos", "Ingrese el nombre de la base de datos:")
        if db_name:
            if not db_name.endswith('.db'):
                db_name += '.db'
            if os.path.exists(db_name):
                try:
                    conn = sqlite3.connect(db_name)
                    conn.close()
                    messagebox.showinfo("Éxito", f"Base de datos '{db_name}' abierta exitosamente.")
                    self.db_name = db_name
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al abrir la base de datos: {e}")
            else:
                messagebox.showwarning("Advertencia", f"La base de datos '{db_name}' no existe.")
        else:
            messagebox.showwarning("Advertencia", "El nombre de la base de datos no puede estar vacío.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
