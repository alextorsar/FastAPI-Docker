FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app

# Instalamos las dependencias necesarias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exponemos el puerto de la aplicación
EXPOSE 8000

# Iniciamos la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]