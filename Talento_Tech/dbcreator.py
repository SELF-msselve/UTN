import sqlite3
import pandas as pd

class DataFrameToSQLite:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_connection(self):
        #Crea una conexión a la base de datos SQLite
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            print(f"Conexión exitosa a {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error al conectar: {e}")
        return conn

    def save_dataframe(self, df, table_name):
        #Guarda un DataFrame de pandas en una tabla de SQLite
        conn = self.create_connection()
        if conn is not None:
            try:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"DataFrame guardado exitosamente en la tabla {table_name}")
            except Exception as e:
                print(f"Error al guardar DataFrame: {e}")
            finally:
                conn.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")

    def read_table(self, table_name):
        #Lee una tabla de la base de datos SQLite si existe """
        conn = self.create_connection()
        if conn is not None:
            try:
                query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    print(f"Tabla {table_name} leída exitosamente")
                    return df
                else:
                    print(f"La tabla {table_name} no existe en la base de datos.")
            except Exception as e:
                print(f"Error al leer la tabla: {e}")
            finally:
                conn.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")
        return None

    def delete_table(self, table_name):
        #Borra una tabla de la base de datos SQLite si existe """
        conn = self.create_connection()
        if conn is not None:
            try:
                query = f"DROP TABLE IF EXISTS {table_name};"
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                print(f"Tabla {table_name} borrada exitosamente")
            except Exception as e:
                print(f"Error al borrar la tabla: {e}")
            finally:
                conn.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")
    
    def list_tables(self):
        #Crea un DataFrame con la lista de todas las tablas de la base de datos
        conn = self.create_connection()
        if conn is not None:
            try:
                query = "SELECT name FROM sqlite_master WHERE type='table';"
                df = pd.read_sql_query(query, conn)
                print("Lista de tablas obtenida exitosamente")
                return df
            except Exception as e:
                print(f"Error al listar las tablas: {e}")
            finally:
                conn.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")
        return None

# Ejemplo de uso:
# Crear un DataFrame de ejemplo
data = {'nombre': ['Alice', 'Bob', 'Charlie'],
        'edad': [24, 27, 22],
        'ciudad': ['Buenos Aires', 'Rosario', 'Córdoba']}
df = pd.DataFrame(data)

# Crear una instancia de la clase y guardar el DataFrame en SQLite
db_manager = DataFrameToSQLite('base_de_datos.db')
db_manager.save_dataframe(df, 'tabla_4')

# Leer la tabla de la base de datos
df_leido = db_manager.read_table('mi_tabla')
if df_leido is not None:
    print(df_leido)

# Listar todas las tablas de la base de datos
df_tablas = db_manager.list_tables()
if df_tablas is not None:
    print(df_tablas)

# Borrar la tabla de la base de datos
db_manager.delete_table('mi_tabla')
