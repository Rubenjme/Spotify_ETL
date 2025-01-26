#------------------------------------------------------------------------------------------
# Este archivo se encarga de cargar los datos transformados en una base de datos PostgreSQL.
#------------------------------------------------------------------------------------------

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv   
import pandas as pd
from Transform import transform_data, validate_data
from Extract import extract_recently_played

# Cargo las credenciales
#load_dotenv()
DB_NAME = os.getenv("POSTGRES_DB")                # Nombre de la base de datos en PostgreSQL 
DB_USER = os.getenv("POSTGRES_USER")              # Usuario de la base de datos
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")      # Contraseña de la base de datos
DB_HOST = os.getenv("POSTGRES_HOST", "localhost") # Host de la base de datos, si no está definida usará localhost
DB_PORT = os.getenv("POSTGRES_PORT", "5432")      # Puerto de la base de datos 

# Función para conectarse a la base de datos 
def connect_to_db():
    try:
        conn = psycopg2.connect(      # Creo la conexión a la base de datos 
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Conexión a la base de datos realizada.")
        return conn
    except Exception as e:
        raise Exception(f"Error al conectar con la base de datos: {e}")

# Crea la tabla en la base de datos si no existe 
def create_table(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS spotify_tracks (
        id SERIAL PRIMARY KEY,
        track_id VARCHAR(255) UNIQUE NOT NULL,
        date DATE NOT NULL,
        artist_name VARCHAR(255) NOT NULL,
        count INTEGER NOT NULL   
    );
    """
    try:
        with conn.cursor() as cursor:               # Creo un cursor para ejecutar la consulta 
            cursor.execute(create_table_query)      # Ejecuto la consulta 
            conn.commit()                           # Confirmo los cambios en la base de datos 
            print("Tabla creada (o ya existe).")
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error al crear la tabla: {e}")

# Carga los datos transformados en la tabla 
def load_data_to_db(conn, df):
    insert_query = """
    INSERT INTO spotify_tracks (track_id, date, artist_name, count)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (track_id) DO NOTHING;
    """
    try:
        with conn.cursor() as cursor:
            for _, row in df.iterrows():                                                                 # Itero sobre las filas del DataFrame 
                cursor.execute(insert_query, (row["ID"], row["date"], row["artist_name"], row["count"])) # Ejecuto la consulta
            conn.commit()
            print("Datos cargados exitosamente.")
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error al cargar los datos: {e}")


if __name__ == "__main__":
    # Extraer y transformar los datos
    raw_data = extract_recently_played()            # Extraigo los datos de la API de Spotify 
    validate_data(raw_data)                         # Valido los datos extraídos 
    transformed_data = transform_data(raw_data)     # Transformo los datos extraídos 

    # Conexión a la base de datos y carga de los datos
    conn = connect_to_db()
    create_table(conn)
    load_data_to_db(conn, transformed_data)   # Cargo los datos transformados en la base de datos 

    conn.close() # Cierro la conexión a la base de datos
