# Spotify ETL Pipeline con Airflow y Docker

Este proyecto consiste en un pipeline **ETL** (Extract, Transform, Load) para recopilar, validar y almacenar los datos de reproducciones en las últimas 24 horas de canciones de Spotify en una base de datos **PostgreSQL**, utilizando **Airflow** como orquestador y **Docker** como plataforma de contenedores.

## Descripción

El proyecto se encarga de:
1. **Extraer** la lista de canciones reproducidas en las últimas 24 horas desde la API de Spotify.
2. **Transformar** y **validar** los datos (eliminar duplicados, normalizar campos, agrupar por fecha y artista, etc.).
3. **Cargar** la información en una tabla de la base de datos PostgreSQL.
4. **Automatizar** todo el proceso con Airflow, permitiendo programar la ejecución diaria (o la frecuencia que elijas).

## Objetivos

- Automatizar la obtención de datos de reproducciones de Spotify.
- Organizar y centralizar la información en una base de datos relacional (PostgreSQL).
- Garantizar la calidad de los datos mediante validaciones y transformaciones.
- Facilitar la reproducibilidad y despliegue mediante contenedores Docker.
- Aprender y demostrar conocimientos de Airflow, Docker y Python en un flujo de trabajo ETL real.

## Arquitectura
  <div align="center">
     <img src="https://github.com/user-attachments/assets/9412808c-b06a-4c12-9ba8-bd270ba29b42">
  </div>

## Configuración inicial - Proceso de extracción de tokens 

Para poder extraer la lista de canciones de Spotify, es necesario obtener un token que nos dé acceso a la API de Spotify. El proceso es el siguiente:

1. **Crear una aplicación en [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)**
   - Obtén tu **Client ID** y **Client Secret**.
   - Registra una **Redirect URI** (por ejemplo, 'http://localhost:8888/callback').
  <div align="center">
     <img src="https://github.com/user-attachments/assets/f68cf581-fbc9-45dc-818e-dda962e3c265">
  </div>

  <div align="center">
     <img src="https://github.com/user-attachments/assets/9bbbee4b-23ac-4675-95ce-7600e4997605">
  </div>

2. **Definir variables de entorno**  
   Crea un archivo `.env` con las siguientes claves (entre otras que uses para Postgres):
   ```dotenv
   SPOTIFY_CLIENT_ID=TU_CLIENT_ID
   SPOTIFY_CLIENT_SECRET=TU_CLIENT_SECRET
   REDIRECT_URI=http://localhost:8888/callback
   SPOTIFY_AUTH_CODE=          # Se rellena después de paso 3
   SPOTIFY_REFRESH_TOKEN=      # Se rellenará tras AccessToken.py

3. **Ejecutar AuthCodeReq.py**
   
   Se usa solo la primera vez para obtener un **Authorization Code** de Spotify, abriendo el navegador y solicitando permiso al usuario.  
   Tras autorizar, Spotify redirige a REDIRECT_URI con un código de autorización en la URL.
   Copia ese code= (llamado Authorization Code) y pégalo en tu .env como SPOTIFY_AUTH_CODE.
   <div align="center">
     <img src="https://github.com/user-attachments/assets/f89144d9-9057-4337-8639-2e6a3ed582a5">
  </div>

5. **Ejecutar AccessToken.py**

   También solo la primera vez, intercambia el authorization code por un access token y un refresh token.  
   Intercambia tu SPOTIFY_AUTH_CODE por un Access Token y un Refresh Token.
   Copia el refresh_token que aparezca en pantalla y pégalo en .env como SPOTIFY_REFRESH_TOKEN.
   A partir de ahora, no volverás a usar AccessToken.py salvo que necesites regenerar tokens.

7. **Uso de RefreshToken.py en la ETL**

   Cada vez que se ejecute el pipeline, RefreshToken.py obtendrá un nuevo Access Token usando SPOTIFY_REFRESH_TOKEN.
   Así se evitan problemas de caducidad y no se requiere intervención del usuario.
   https://github.com/user-attachments/assets/9bbbee4b-23ac-4675-95ce-7600e4997605
   <div align="center">
     <img src="https://github.com/user-attachments/assets/931effc8-0917-4055-b879-7c01d7711b01">
  </div>

Una vez configurado este flujo de autenticación, el pipeline podrá extraer datos de Spotify sin interrupciones.

## Funcionamiento

### Sin automatización

1. Ejecuta **Extract.py**

   Llama a la API de Spotify (con el token renovado) y devuelve un DataFrame con las reproducciones recientes (últimas 24 horas). 
   <div align="center">
     <img src="https://github.com/user-attachments/assets/af3ff0d9-0f20-46b4-b14b-c01cdf9f9c54">
  </div>
3. Ejecuta **Transform.py**
   
   Valida, limpia y normaliza los datos (por ejemplo, pasa los campos a mayúsculas y agrupa por fecha y artista, etc).
    <div align="center">
     <img src="https://github.com/user-attachments/assets/8c8aee05-ce70-47e2-adb0-5f3cb4ce6f07">
  </div>

4. Ejecuta **Load.py**

   Carga los datos resultantes en la tabla `spotify_tracks` de la base de datos PostgreSQL.
   <div align="center">
     <img src="https://github.com/user-attachments/assets/7c061bdf-10fd-43e9-b177-0905a56a0f87">
  </div>

6. Comprueba en pgAdmin de PostgreSQL

   Ejecutamos pgAdmin y buscamos la base de datos para confirmar que las canciones han sido cargadas correctamente en la tabla spotify_tracks.
   <div align="center">
     <img src="https://github.com/user-attachments/assets/0e9e8bf2-7007-49ae-9450-d653cb129d80">
  </div>


Si de repente escuchamos alguna nueva canción en Spotify (por ejemplo "Thunder - Imagine Dragons") y volvemos a realizar el proceso, se puede ver como la lista se actualiza. 

Salida de Extract.py:
   <div align="center">
     <img src="https://github.com/user-attachments/assets/9bdbf5f7-84d4-46bf-ae58-baed73d9ead4">
  </div>

Salida de Transform.py:
   <div align="center">
     <img src="https://github.com/user-attachments/assets/69a25b14-b30d-422f-a713-8542a48d93e4">
  </div>

Registro en PostgreSQL:
   <div align="center">
     <img src="https://github.com/user-attachments/assets/b1d464e4-0f56-4f4c-948f-a7eac77dcd10">
  </div>

### Con automatización

1. Levantamos los servicios de Docker con los comandos:

   - docker-compose build
   - docker-compose up -d
   
   ![docker](https://github.com/user-attachments/assets/6839fee2-27f2-4c7b-bba6-5f3ec3ad939e)


3. Accede a la interfaz de Airflow

   Entramos con el usuario y contraseña configurados (Airflow en ambos casos).
   Vemos como el DAG creado aparece.
   
   ![dag](https://github.com/user-attachments/assets/3d32276f-7ef3-4bef-9f28-b8fe80c28b33)

   Activamos el DAG para que se ejecute.

   ![dagfuncionando](https://github.com/user-attachments/assets/91c3b1d7-4725-48b8-b140-bca8059f74cc)

4. Comprobamos en base de datos que aparece la canción de Imagine Dragons, además de otras nuevas.
   
   Se puede ver que también se han creado diversas tablas que pertenecen a Airflow, esto se debe a que se configuró que sus datos se almacenarán también en la misma base de datos, próximamente lo cambiaré para que los datos de Airflow se encuentren en una base de datos    diferente.

   ![13  postgreDag](https://github.com/user-attachments/assets/9093d565-53ad-417e-8d15-ab3d35ed72f4)


### ⚠️Tener en cuenta

Un problema del que no me percaté fue que tenía 2 servicios activos para un mismo puerto (5432), por lo que al ejecutar la ETL los datos no se cargaban en la BBDD.

<div align="center">
  <img src="https://github.com/user-attachments/assets/3345cf53-3198-4e7f-99f0-9762ad1b01b8">
</div>

Para resolverlo solo hay que detener el servicio de PostgreSQL (Win+R -> services.msc -> Detener el servicio), esto impedirá su uso en local mientras siga detenido.


## Pasos para ejecutar el proyecto

1. Clonar el repositorio

2. Configurar variables de entorno

3. Obtener el refresh token (solo la primera vez)

4. Construir e iniciar servicios con Docker Compose
  
5. Inicializar la base de datos de Airflow (solo la primera vez)

6. Acceder a la interfaz de Airflow

7. Verificar la carga de datos

## Próximas mejoras
- Bases de datos individuales: Separar los datos de Airflow en otra base de datos distinta a la que se suben los datos de Spotify.
- Alertas: Configurar Airflow para que mande alertas si falla el DAG.
- Dashboard: Integrar un BI (Tableau, Power BI) para visualizar la música reproducida.
- Extender alcance: Analizar datos históricos, popularidad de artistas, etc.
