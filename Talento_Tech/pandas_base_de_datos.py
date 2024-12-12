
import pandas as pd
import sqlite3

# Crear un DataFrame de ejemplo con 3 columnas y 10 filas
data = {
    'Columna1': range(11, 21),
    'Columna2': [f'Dato{i}' for i in range(1, 11)],
    'Columna3': [i * 10 for i in range(1, 11)]
}
df = pd.DataFrame(data)

# Clase para guardar y leer DataFrames en una base de datos SQLite
class DataFrameToSQLite:
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
        # Leer la tabla de la base de datos en un DataFrame
        dataframe = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        # Cerrar la conexión
        conn.close()
        return dataframe

# Crear una instancia de la clase
db_saver = DataFrameToSQLite('mi_base_de_datos.db')

# Guardar el DataFrame en la base de datos
db_saver.save_to_db('mi_tabla_2', df)

# Leer la tabla de la base de datos en un DataFrame
df_leido = db_saver.read_from_db('mi_tabla')
df_leido_2 = db_saver.read_from_db('mi_tabla_2')

print("El DataFrame original ha sido guardado en la base de datos SQLite.")
print("El DataFrame leído de la base de datos es:")
print(df_leido)
print(df_leido_2)

