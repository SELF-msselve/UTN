import pandas as pd
import sqlite3

class data_base:
    def __init__(self, db_name):
        self.db_name = db_name

    def save_to_db(self, table_name, dataframe):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(self.db_name)
        # Guardar el DataFrame en la base de datos
        dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
        # Cerrar la conexión
        conn.close()

    def read_from_db(self, table_name):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone() is None:
            print(f"La tabla '{table_name}' no existe.")
            conn.close()
            return None
                
        # Leer la tabla de la base de datos en un DataFrame
        dataframe = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        # Cerrar la conexión
        conn.close()
        return dataframe

    def list_tables(self):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Obtener los nombres de todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Convertir a DataFrame
        df_tables = pd.DataFrame(tables, columns=['Table_Name'])
        
        # Cerrar la conexión
        conn.close()
        return df_tables

    def delete_table(self, table_name):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone() is None:
            print(f"La tabla '{table_name}' no existe.")
        else:
            # Eliminar la tabla
            cursor.execute(f"DROP TABLE {table_name}")
            print(f"La tabla '{table_name}' ha sido eliminada.")
        
        # Cerrar la conexión
        conn.commit()
        conn.close()
