#!/bin/bash

# Script de configuración para entorno de desarrollo de Serena MVP
# Uso: ./scripts/setup_dev.sh

echo "Configurando entorno de desarrollo para Serena MVP..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "Error: Node.js no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "Error: pip no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si npm está instalado
if ! command -v npm &> /dev/null; then
    echo "Error: npm no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

echo "Creando archivo .env para backend si no existe..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "Archivo .env creado. Por favor, edítalo con tus configuraciones."
else
    echo "El archivo .env ya existe."
fi

echo "Creando archivo .env para frontend si no existe..."
if [ ! -f frontend/.env ]; then
    echo "VITE_API_URL=http://localhost:5000/api" > frontend/.env
    echo "Archivo .env creado."
else
    echo "El archivo .env ya existe."
fi

echo "Configurando entorno virtual de Python..."
if [ ! -d backend/venv ]; then
    python3 -m venv backend/venv
    echo "Entorno virtual creado."
else
    echo "El entorno virtual ya existe."
fi

echo "Activando entorno virtual..."
source backend/venv/bin/activate

echo "Instalando dependencias de Python..."
pip install -r backend/requirements.txt

echo "Instalando dependencias de Node.js..."
cd frontend && npm install && cd ..

echo "Creando directorio instance para SQLite si no existe..."
mkdir -p backend/instance

echo "Inicializando base de datos..."
cd backend
export FLASK_APP=run.py
export FLASK_ENV=development
python -c "from app import db; db.create_all()"
cd ..

echo "Configurando migraciones de base de datos..."
cd backend
if [ ! -d migrations ]; then
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    echo "Migraciones inicializadas."
else
    echo "Directorio de migraciones ya existe."
fi
cd ..

echo "Configuración completada con éxito!"
echo "Para iniciar el backend, ejecuta: cd backend && source venv/bin/activate && flask run"
echo "Para iniciar el frontend, ejecuta: cd frontend && npm run dev"