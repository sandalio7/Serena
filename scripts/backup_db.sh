#!/bin/bash

# Script para crear respaldo de la base de datos SQLite
# Uso: ./scripts/backup_db.sh

# Configurar directorio de respaldos
BACKUP_DIR="backups"
BACKUP_FILE="serena_db_$(date +%Y%m%d_%H%M%S).sqlite"
DB_PATH="backend/instance/app.db"

# Verificar si el directorio de respaldos existe
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "Directorio de respaldos creado: $BACKUP_DIR"
fi

# Verificar si la base de datos existe
if [ ! -f "$DB_PATH" ]; then
    echo "Error: Base de datos no encontrada en $DB_PATH"
    exit 1
fi

# Crear respaldo
echo "Creando respaldo de la base de datos..."
cp "$DB_PATH" "$BACKUP_DIR/$BACKUP_FILE"

# Comprimir respaldo
echo "Comprimiendo respaldo..."
gzip "$BACKUP_DIR/$BACKUP_FILE"

echo "Respaldo completado: $BACKUP_DIR/${BACKUP_FILE}.gz"

# Eliminar respaldos antiguos (mantener los últimos 5)
echo "Limpiando respaldos antiguos..."
ls -t "$BACKUP_DIR"/*.gz | tail -n +6 | xargs -r rm

echo "Proceso de respaldo finalizado con éxito!"