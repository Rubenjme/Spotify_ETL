#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Este archivo contiene el código para renovar el access token usando el refresh token. Así mantenemos el flujo de autenticación separado del resto del código.
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

import requests
from dotenv import load_dotenv
import os

# Cargo las credenciales desde el archivo .env
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

# Renueva el access token usando el refresh token
def get_access_token():
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]
    else:
        raise Exception(f"Error al renovar el token: {response.status_code}, {response.text}")

# Ejecuta la función principal
if __name__ == "__main__":
    print("Token de acceso renovado:", get_access_token())
