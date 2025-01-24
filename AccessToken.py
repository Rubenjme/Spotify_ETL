#---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Este script tiene intercambia un auth code por un access token y un refresh token. Solo es necesario ejecutarlo una vez para obtener el refresh token inicial.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

import os
import requests
from dotenv import load_dotenv

# Cargo las credenciales desde el archivo .env
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_CODE = os.getenv("SPOTIFY_AUTH_CODE") # Código de autorización obtenido manualmente desde el navegador (Caduca al poco tiempo)

# Intercambia el código de autorización por un token de acceso
def get_access_token(auth_code):

    TOKEN_URL = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        token_info = response.json()
        print("Access Token:", token_info["access_token"])
        print("Refresh Token:", token_info["refresh_token"])
        return token_info
    else:
        raise Exception(f"Error al obtener el token: {response.status_code}, {response.text}")

# Ejecuta la función principal
if __name__ == "__main__":
    token_info = get_access_token(AUTH_CODE)
    print(token_info)
