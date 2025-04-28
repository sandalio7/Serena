FROM node:16-alpine

WORKDIR /app

# Copiar archivos de configuración
COPY frontend/package.json frontend/package-lock.json* ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente
COPY frontend/ .

# Construir la aplicación
RUN npm run build

# Instalar servidor para producción
RUN npm install -g serve

# Puerto de la aplicación
EXPOSE 3000

# Comando para iniciar la aplicación
CMD ["serve", "-s", "dist", "-l", "3000"]