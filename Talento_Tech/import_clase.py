import pandas as pd   
import sqlite3  
import clase_db as clasedb

db_saver = clasedb.DataFrameToSQLite('mi_base_de_datos.db')

def funcion_ver():
    df_leido = db_saver.read_from_db('mi_tabla')
    df_leido_2 = db_saver.read_from_db('mi_tabla_2')

    print("El DataFrame original ha sido guardado en la base de datos SQLite.")
    print("El DataFrame leído de la base de datos es:")
    print(df_leido)
    print(df_leido_2)

    df_of_df = [df_leido, df_leido_2]

    print(df_of_df)
    print("El DataFrame 2 leído de la base de datos es:")
    print(df_of_df[1])

def funcion_ver2():
    df_indice = db_saver.list_tables()
    print(df_indice)

def funcion_include(nombre_tabla):
    data = {
        'Columna1': range(1, 11),
        'Columna2': [f'{nombre_tabla} {i}' for i in range(1, 11)],
        'Columna3': [i * 10 for i in range(1, 11)]
    }
    nombre = 'Poti-' + nombre_tabla
    df = pd.DataFrame(data)
    db_saver.save_to_db(nombre, df)

def funcion_delete(nombre_tabla):
    db_saver.delete_table(nombre_tabla)

funcion_include('Tabla_7')  
funcion_ver2  
funcion_delete('Tabla_8') 
funcion_ver2()
