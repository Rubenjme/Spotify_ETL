# Spotify ETL Pipeline con Airflow y Docker

Este proyecto consiste en un pipeline **ETL** (Extract, Transform, Load) para recopilar, validar y almacenar los datos de reproducciones en las últimas 24 horas de canciones de Spotify en una base de datos **PostgreSQL**, utilizando **Airflow** como orquestador y **Docker** como plataforma de contenedores.

## Descripción

El proyecto se encarga de:
1. **Extraer** la lista de canciones reproducidas en las últimas 24 horas desde la API de Spotify.
2. **Transformar** y **validar** los datos (eliminar duplicados, normalizar campos, agrupar por fecha y artista, etc.).
3. **Cargar** la información en una tabla de la base de datos PostgreSQL.
4. **Orquestar** todo el proceso con Airflow, permitiendo programar la ejecución diaria (o la frecuencia que elijas).

## Objetivos

- Automatizar la obtención de datos de reproducciones de Spotify.
- Organizar y centralizar la información en una base de datos relacional (PostgreSQL).
- Garantizar la calidad de los datos mediante validaciones y transformaciones.
- Facilitar la reproducibilidad y despliegue mediante contenedores Docker.
- Aprender y demostrar conocimientos de Airflow, Docker y Python en un flujo de trabajo ETL real.

## Arquitectura

Esquema aquí---


1. **AuthCodeReq.py**  
   Se usa **solo la primera vez** para obtener un **Authorization Code** de Spotify, abriendo el navegador y solicitando permiso al usuario.  
2. **AccessToken.py**  
   También **solo la primera vez**, intercambia el Authorization Code por un **Access Token** y un **Refresh Token**. El **Refresh Token** no expira tan rápido y nos permite pedir nuevos **Access Tokens** sin volver a molestar al usuario.  
3. **RefreshToken.py**  
   En la ejecución diaria (ETL), se usa el **Refresh Token** para solicitar un **Access Token** actualizado y poder llamar a la API de Spotify.  
4. **Extract.py**  
   Llama a la API de Spotify (con el token renovado) y devuelve un DataFrame con las reproducciones recientes (últimas 24 horas).  
5. **Transform.py**  
   Valida, limpia y normaliza los datos (por ejemplo, pasa los campos a mayúsculas y agrupa por fecha y artista).  
6. **Load.py**  
   Carga los datos resultantes en la tabla `spotify_tracks` de la base de datos PostgreSQL.  
7. **Airflow**  
   Controla la programación y el orden de ejecución de `Extract -> Transform -> Load`.  

## Proceso de extracción de tokens (Configuración inicial)

Para poder extraer la lista de canciones de Spotify, es necesario obtener un token que nos dé acceso a la **API de Spotify**. El proceso es el siguiente:

1. **Crear una aplicación en [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)**
   - Obtén tu **Client ID** y **Client Secret**.
   - Registra una **Redirect URI** (por ejemplo, 'http://localhost:8888/callback').

2. **Definir variables de entorno**  
   Crea un archivo `.env` con las siguientes claves (entre otras que uses para Postgres):
   ```dotenv
   SPOTIFY_CLIENT_ID=TU_CLIENT_ID
   SPOTIFY_CLIENT_SECRET=TU_CLIENT_SECRET
   REDIRECT_URI=http://localhost:8888/callback
   SPOTIFY_AUTH_CODE=          # Se rellena después de paso 3
   SPOTIFY_REFRESH_TOKEN=      # Se rellenará tras AccessToken.py

3. **Ejecutar AuthCodeReq.py**

Abre el navegador y pide permiso al usuario.
Tras autorizar, Spotify redirige a REDIRECT_URI con un código de autorización en la URL.
Copia ese code= (llamado Authorization Code) y pégalo en tu .env como SPOTIFY_AUTH_CODE.

4. Ejecutar AccessToken.py
Intercambia tu SPOTIFY_AUTH_CODE por un Access Token y un Refresh Token.
Copia el refresh_token que aparezca en pantalla y pégalo en .env como SPOTIFY_REFRESH_TOKEN.
A partir de ahora, no volverás a usar AccessToken.py salvo que necesites regenerar tokens.

5. Uso de RefreshToken.py en la ETL
Cada vez que se ejecute el pipeline, RefreshToken.py obtendrá un nuevo Access Token usando SPOTIFY_REFRESH_TOKEN.
Así se evitan problemas de caducidad y no se requiere intervención del usuario.


Una vez configurado este flujo de autenticación, el pipeline podrá extraer datos de Spotify sin interrupciones.

## Pasos para ejecutar el proyecto

1. Clonar el repositorio

2. Configurar variables de entorno

3. Obtener el refresh token (solo la primera vez)

4. Construir e iniciar servicios con Docker Compose
  
5. Inicializar la base de datos de Airflow (solo la primera vez)

6. Acceder a la interfaz de Airflow

7. Verificar la carga de datos


## Flujo de trabajo

Autenticación Inicial:
Ejecutas AuthCodeReq.py para obtener el Authorization Code.
Luego, ejecutas AccessToken.py para intercambiar el Authorization Code por los Access y Refresh Tokens.
Almacenas el Refresh Token en el archivo .env para uso futuro.

Ejecución del Pipeline ETL:
Airflow programa la ejecución diaria del DAG Spotify_etl_dag.py.
RefreshToken.py obtiene un Access Token actualizado.
Extract.py extrae los datos recientes de Spotify utilizando el Access Token.
Transform.py valida y transforma los datos extraídos.
Load.py carga los datos transformados en la base de datos spotify_data en PostgreSQL.

Almacenamiento y Acceso:
Los datos se almacenan en la tabla spotify_tracks dentro de la base de datos spotify_data.
Puedes acceder a estos datos a través de herramientas como PgAdmin 4 para análisis y visualización.

## Próximas mejoras
- Bases de datos individuales: Separar los datos de Airflow en otra base de datos distinta a la que se suben los datos de Spotify.
- Alertas: Configurar Airflow para que mande alertas si falla el DAG.
- Dashboard: Integrar un BI (Tableau, Power BI) para visualizar la música reproducida.
- Extender alcance: Analizar datos históricos, popularidad de artistas, etc.
