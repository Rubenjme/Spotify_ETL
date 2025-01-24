from Extract import extract_recently_played
from Transform import validate_data, transform_data
from Load import connect_to_db, create_table, load_data_to_db

# Ejecuta el pipeline completo
def etl_pipeline():
    
    raw_data = extract_recently_played() # Extracción de datos 

    # Validación y transformación de datos 
    validate_data(raw_data)
    transformed_data = transform_data(raw_data)

    # Carga de datos a la base de datos 
    conn = connect_to_db()
    create_table(conn)
    load_data_to_db(conn, transformed_data)
    conn.close()

# Ejecuto el pipeline ETL
if __name__ == "__main__":
    etl_pipeline()
