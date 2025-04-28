#!/bin/bash

# Script de despliegue para Serena MVP
# Uso: ./scripts/deploy.sh [dev|prod]

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Error: Docker no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar el entorno especificado
ENV=${1:-prod}
if [[ "$ENV" != "dev" && "$ENV" != "prod" ]]; then
    echo "Error: Entorno no válido. Use 'dev' o 'prod'."
    exit 1
fi

echo "Desplegando Serena MVP en entorno: $ENV"

# Verificar si el archivo .env.docker existe
if [ ! -f docker/.env.docker ]; then
    echo "Error: Archivo docker/.env.docker no encontrado. Por favor, créalo antes de continuar."
    exit 1
fi

# Copiar archivo .env.docker
cp docker/.env.docker .env

# Desplegar usando Docker Compose
echo "Construyendo imágenes Docker..."
if [[ "$ENV" == "dev" ]]; then
    docker-compose -f docker/docker-compose.dev.yml build
else
    docker-compose -f docker/docker-compose.prod.yml build
fi

echo "Iniciando contenedores..."
if [[ "$ENV" == "dev" ]]; then
    docker-compose -f docker/docker-compose.dev.yml up -d
else
    docker-compose -f docker/docker-compose.prod.yml up -d
fi

echo "Aplicando migraciones..."
if [[ "$ENV" == "dev" ]]; then
    docker-compose -f docker/docker-compose.dev.yml exec backend flask db upgrade
else
    docker-compose -f docker/docker-compose.prod.yml exec backend flask db upgrade
fi

echo "Despliegue completado con éxito!"
if [[ "$ENV" == "dev" ]]; then
    echo "La aplicación está disponible en http://localhost:3000"
else
    echo "La aplicación está desplegada en producción"
fi