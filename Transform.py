#---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Este script se encarga de validar y transformar los datos extraídos de la API.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
from Extract import extract_recently_played # Importa los datos desde Extract.py

# Esta función valida los datos extraídos
def validate_data(df):
    # Verifico si el DataFrame está vacío
    if df.empty:
        raise Exception("El Dataframe está vacío. Sin datos para procesar.")

    # Verifico que en la columna 'played_at' no haya valores duplicados
    if not pd.Series(df["played_at"]).is_unique:
        raise Exception("Datos duplicados encontrados en la columna 'played_at'.")

    # Verifico que no haya valores nulos
    if df.isnull().values.any():
        raise Exception("Hay valores nulos en los datos extraídos.")

    print("Los datos han sido validados.")
    return True


# Esta función transforma los datos extraídos en un nuevo DataFrame
def transform_data(df):
    df["song_name"] = df["song_name"].str.upper()       # Convierto a mayúsculas los nombres de las canciones
    df["artist_name"] = df["artist_name"].str.upper()   # Convierto a mayúsculas los nombres de los artistas
    
    grouped_df = df.groupby(["date", "artist_name"], as_index=False).count()            # Agrupo los datos por fecha y nombre del artista
    grouped_df.rename(columns={"played_at": "count"}, inplace=True)                          # Renombro la columna 'played_at' a 'count' (cantidad de reproducciones) 
    grouped_df["ID"] = grouped_df["date"].astype(str) + "-" + grouped_df["artist_name"] # Creo una clave primaria basada en la fecha y el nombre del artista 
    
    transformed_df = grouped_df[["ID", "date", "artist_name", "count"]]                            # Selecciono y reorganizo las columnas
    transformed_df = transformed_df.sort_values(by="date", ascending=False).reset_index(drop=True) # Ordeno por fecha de forma descendente (de lo más reciente a lo más antiguo)

    print("Los datos han sido transformados.")
    return transformed_df


if __name__ == "__main__":
    df = extract_recently_played()              # Extrae los datos

    validate_data(df) # Llamo a la función para validar los datos

    transformed_df = transform_data(df) # Llamo a la función para aplicar transformaciones a los datos  

    # Imprimo los datos transformados
    print("Datos transformados:")
    print(transformed_df)
