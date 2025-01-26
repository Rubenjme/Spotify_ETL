#-------------------------------------------------------------------------------
# Este archivo recopila los pasos anteriores y ejecuta el pipeline ETL completo.
#-------------------------------------------------------------------------------
from Extract import extract_recently_played
from Transform import validate_data, transform_data
from Load import connect_to_db, create_table, load_data_to_db
import logging

# Ejecuta el pipeline completo
def etl_pipeline():
    logging.basicConfig(level=logging.INFO)
    logging.info("Iniciando el pipeline ETL")

    logging.info("Comenzando extracción de datos")
    raw_data = extract_recently_played() # Extracción de datos 
    logging.info("Datos extraídos")

    # Validación y transformación de datos 
    logging.info("Comenzando validación y transformación de datos")
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
