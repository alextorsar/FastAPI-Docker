FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app

# Instalamos las dependencias necesarias
RUN pip install pymongo

# Exponemos el puerto de la aplicación
EXPOSE 8000

# Iniciamos la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]