# Crear un módulo para la conexión a la base de datos
# filepath: modules/db_connection.py
import mysql.connector

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='Doker367.',  
            database='tienda'  
        )
        if conexion.is_connected():
            return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None