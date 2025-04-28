FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY backend/ .

# Variables de entorno
ENV FLASK_APP="run.py"
ENV FLASK_ENV="production"
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL="sqlite:///instance/app.db"

# Puerto de la aplicación
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]