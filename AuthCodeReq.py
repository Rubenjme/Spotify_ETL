#-------------------------------------------------------------------------------------------------------------------------------------------------
# Este script se encargará de conseguir el token de autorización (solo es necesario hacerlo una vez) para poder extraer datos de la API de Spotify.
#--------------------------------------------------------------------------------------------------------------------------------------------------
# Proceso explicado -> https://developer.spotify.com/documentation/web-api/tutorials/code-flow

from dotenv import load_dotenv
import os
import webbrowser

# Cargo las credenciales desde el archivo .env
load_dotenv() 
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")  # Debe coincidir con la URI configurada en Spotify Dashboard
SCOPES = "user-read-recently-played"


def request_authorization_code():
    """Solicita al usuario que autorice la aplicación"""
    AUTH_URL = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    print(f"Abriendo el navegador para autorizar la aplicación...\n{AUTH_URL}")
    webbrowser.open(AUTH_URL)

if __name__ == "__main__":
    request_authorization_code()
