#--------------------------------------------------------------------------------------
# Este script se encarga de extraer las canciones reproducidas en las últimas 24 horas. 
#--------------------------------------------------------------------------------------
# pip install unidecode -> para eliminar carácteres extraños

import requests
import pandas as pd
from unidecode import unidecode
from datetime import datetime, timedelta
from RefreshToken import get_access_token  # Usa la función de refresh de token

# Función que extrae las canciones reproducidas recientemente del usuario
def extract_recently_played():
    access_token = get_access_token()  # Obtengo el token renovado

    # Configuro los encabezados para la solicitud a la API
    headers = { 
        "Authorization": f"Bearer {access_token}",
    }

    # Configuro el rango de tiempo (últimas 24 horas)
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # URL de la API para canciones reproducidas recientemente
    url = f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={yesterday_unix_timestamp}" # Limito a 50 canciones para no exceder el límite de la API 
    response = requests.get(url, headers=headers)

    # Verifica si la solicitud fue exitosa y extrae los datos si es así 
    if response.status_code == 200:
        data = response.json()

        # Extraigo los datos relevantes y los guardo en un diccionario 
        song_dict = {
            "song_name": [unidecode(song["track"]["name"]) for song in data["items"]],
            "artist_name": [unidecode(song["track"]["album"]["artists"][0]["name"]) for song in data["items"]],
            "played_at": [song["played_at"] for song in data["items"]],
            "timestamp": [song["played_at"][0:10] for song in data["items"]],
        }

        song_df = pd.DataFrame(song_dict) # Creo un DataFrame con los datos extraídos 
        return song_df
    else:
        raise Exception(f"Error al obtener canciones: {response.status_code}, {response.text}")


# Ejecuta la extracción
if __name__ == "__main__":
    df = extract_recently_played()
    print("Canciones reproducidas en las últimas 24 horas:")
    print(df)

