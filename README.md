
## Requisitos

- Docker (versión 18 o superior)
- Python 3.11.2

## Instalación

1. Clona este repositorio en tu ordenador
2. Navega a la carpeta del proyecto

## Uso

1. Levanta la API mediante Docker utilizando el comando: `docker-compose up`.
2. Accede a la API en tu navegador web en la dirección `http://localhost:8000/docs`.
3. Detén los contenedores ejecutando el comando `docker-compose down` cuando hayas terminado de utilizar la API.

## Información adicional

- La carpeta `app/routes` contiene los archivos con las rutas de la API.
- La carpeta `app/models` contiene los archivos con los modelos de la base de datos.
- La carpeta `app/schemas` contiene los archivos con los esquemas de datos para la validación de entradas y salidas.
- El archivo `Dockerfile` define la configuración de la imagen de Docker.
- El archivo `docker-compose.yml` define la configuración para levantar los contenedores.
