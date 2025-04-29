# Despliegue en Producción

Esta guía detalla el proceso para desplegar Serena MVP en un entorno de producción.

## Requisitos Previos

- Servidor Linux (Ubuntu 20.04 LTS recomendado)
- Docker y Docker Compose instalados
- Dominio configurado con registros DNS apuntando al servidor
- Certificado SSL (recomendado Let's Encrypt)
- Cuentas de servicio configuradas:
  - Google Cloud Platform (para API de Gemini)
  - Twilio o MessageBird (para integración con WhatsApp)

## 1. Preparación del Servidor

### 1.1. Actualización del Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2. Instalación de Dependencias

```bash
# Instalar Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Añadir usuario al grupo docker (evita usar sudo con docker)
sudo usermod -aG docker $USER
# Aplicar cambios de grupo (o reiniciar sesión)
newgrp docker
```

### 1.3. Configuración de Firewall

```bash
# Instalar UFW si no está instalado
sudo apt install -y ufw

# Configuración básica
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir SSH
sudo ufw allow ssh

# Permitir HTTP y HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activar Firewall
sudo ufw enable
```

## 2. Configuración de Dominio y SSL

### 2.1. Configuración con Certbot (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install -y certbot

# Obtener certificado
sudo certbot certonly --standalone -d tu-dominio.com -d www.tu-dominio.com

# Verificar ubicación de certificados
ls -la /etc/letsencrypt/live/tu-dominio.com/
```

### 2.2. Renovación Automática de Certificados

```bash
# Probar renovación
sudo certbot renew --dry-run

# La renovación automática se configura por defecto como una tarea cron
```

## 3. Despliegue de Serena MVP

### 3.1. Clonar Repositorio

```bash
git clone https://github.com/tu-usuario/serena-project.git
cd serena-project
```

### 3.2. Configurar Variables de Entorno

```bash
cp docker/.env.docker .env

# Editar .env con configuración de producción
nano .env
```

Configura las siguientes variables:

```
# API de Google para Gemini AI
GOOGLE_API_KEY=tu_clave_api_aqui

# Token de verificación para WhatsApp
VERIFY_TOKEN=token-secreto-para-produccion

# Clave secreta para JWT
JWT_SECRET_KEY=clave-secreta-jwt-para-produccion

# Configuración de Base de datos
DATABASE_URL=sqlite:///instance/app.db

# Entorno Flask
FLASK_ENV=production
```

### 3.3. Configurar Nginx para SSL

Edita el archivo `docker/nginx/default.conf`:

```bash
nano docker/nginx/default.conf
```

Reemplaza el contenido con esta configuración para HTTPS:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redireccionar todo el tráfico HTTP a HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Configuración SSL
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    
    # Configuración HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Backend API
    location /api {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Webhook específico para WhatsApp
    location /api/webhook {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3.4. Actualizar Docker Compose para SSL

Edita `docker/docker-compose.prod.yml`:

```bash
nano docker/docker-compose.prod.yml
```

Añade los volúmenes para los certificados SSL:

```yaml
nginx:
  # ... (configuración existente)
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt:ro
    - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
```

### 3.5. Despliegue con Docker Compose

Usa el script de despliegue:

```bash
./scripts/deploy.sh prod
```

O manualmente:

```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

### 3.6. Verificar Despliegue

```bash
# Verificar que los contenedores están funcionando
docker-compose -f docker/docker-compose.prod.yml ps

# Verificar logs
docker-compose -f docker/docker-compose.prod.yml logs
```

## 4. Configuración de WhatsApp Business API

### 4.1. Con Twilio

1. Accede a la consola de Twilio
2. Configura el Webhook para WhatsApp:
   - URL: `https://tu-dominio.com/api/webhook/whatsapp`
   - Método: `POST`
   - Evento: `Incoming Messages`

### 4.2. Con MessageBird

1. Accede al panel de MessageBird
2. Configura el endpoint de webhook:
   - URL: `https://tu-dominio.com/api/webhook/whatsapp`
   - Método: `POST`

## 5. Monitoreo y Mantenimiento

### 5.1. Configuración de Logs

Configura la rotación de logs:

```bash
sudo nano /etc/logrotate.d/docker-logs

# Añade:
/var/lib/docker/containers/*/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    copytruncate
}
```

### 5.2. Monitoreo Básico

Instala una herramienta de monitoreo básica:

```bash
# Instalar Glances para monitoreo del sistema
sudo apt install -y glances
```

### 5.3. Respaldos Automáticos

Configura un cron job para ejecutar respaldos diarios:

```bash
crontab -e

# Añade:
0 2 * * * /ruta/absoluta/a/serena-project/scripts/backup_db.sh
```

### 5.4. Actualización de la Aplicación

Para actualizar a una nueva versión:

```bash
# Detener servicios
docker-compose -f docker/docker-compose.prod.yml down

# Actualizar código
git pull

# Reconstruir y reiniciar
docker-compose -f docker/docker-compose.prod.yml up -d --build
```

## 6. Seguridad Adicional

### 6.1. Fail2Ban para Protección de Fuerza Bruta

```bash
# Instalar Fail2Ban
sudo apt install -y fail2ban

# Crear configuración para proteger endpoints sensibles
sudo nano /etc/fail2ban/jail.d/serena-auth.conf

# Añadir:
[serena-auth]
enabled = true
port = http,https
filter = serena-auth
logpath = /var/lib/docker/containers/*/*.log
maxretry = 5
findtime = 300
bantime = 3600
```

### 6.2. Respaldos Externos

Configura respaldos en almacenamiento externo (opcional):

```bash
# Instalar rclone
curl https://rclone.org/install.sh | sudo bash

# Configurar rclone (seguir instrucciones interactivas)
rclone config

# Crear script para respaldo remoto
nano scripts/remote_backup.sh

# Ejemplo de contenido:
#!/bin/bash
BACKUP_DIR="/ruta/a/respaldos"
REMOTE_NAME="tu-remote"
REMOTE_PATH="serena-backups"

# Ejecutar respaldo local primero
/ruta/absoluta/a/serena-project/scripts/backup_db.sh

# Sincronizar con almacenamiento remoto
rclone sync $BACKUP_DIR $REMOTE_NAME:$REMOTE_PATH
```

## 7. Solución de Problemas Comunes

### 7.1. Problemas de Acceso a Base de Datos

Verificar permisos:

```bash
# Verificar permisos del volumen de SQLite
ls -la /ruta/a/serena-project/backend/instance/

# Arreglar permisos si es necesario
sudo chown -R 1000:1000 /ruta/a/serena-project/backend/instance/
```

### 7.2. Problemas con Webhook de WhatsApp

Verificar logs:

```bash
docker-compose -f docker/docker-compose.prod.yml logs backend | grep webhook
```

### 7.3. Problemas con Certificados SSL

Verificar fecha de expiración:

```bash
certbot certificates
```

Forzar renovación si es necesario:

```bash
sudo certbot renew --force-renewal
```

## 8. Escalado (Futuro)

Para futuras necesidades de escalado:

1. **Migrar a PostgreSQL**:
   - Actualizar `DATABASE_URL` en `.env`
   - Ajustar `docker-compose.prod.yml` para incluir un servicio PostgreSQL
   - Ejecutar migraciones

2. **Balanceo de Carga**:
   - Implementar múltiples instancias del backend
   - Configurar un balanceador de carga como HAProxy o usar servicios como CloudFlare

3. **Caché**:
   - Implementar Redis para caché de sesiones y datos frecuentes
   - Ajustar configuración de Flask para usar Redis

## 9. Despliegue en Servicios en la Nube (Alternativa)

### 9.1. AWS

1. **Configuración de EC2**:
   - Crea una instancia EC2 (t3.small o superior)
   - Configura grupos de seguridad para puertos 22, 80, 443
   - Sigue los pasos 1-6 de esta guía

2. **Alternativa con ECS/Fargate**:
   - Sube imágenes Docker a ECR
   - Configura un servicio ECS con Fargate
   - Utiliza ELB para balanceo de carga
   - Configura RDS para PostgreSQL (en producción a escala)

### 9.2. Google Cloud Platform

1. **Configuración de Compute Engine**:
   - Crea una instancia VM (e2-medium o superior)
   - Configura reglas de firewall para puertos 22, 80, 443
   - Sigue los pasos 1-6 de esta guía

2. **Alternativa con Cloud Run**:
   - Sube imágenes Docker a Container Registry
   - Despliega el backend en Cloud Run
   - Despliega el frontend en Cloud Run o Firebase Hosting
   - Utiliza Cloud SQL para PostgreSQL (en producción a escala)

### 9.3. Heroku (Opción simple)

```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Iniciar sesión
heroku login

# Crear aplicaciones
heroku create serena-backend
heroku create serena-frontend

# Configurar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev -a serena-backend

# Configurar variables de entorno
heroku config:set GOOGLE_API_KEY=tu_clave_api -a serena-backend
heroku config:set JWT_SECRET_KEY=tu_clave_secreta -a serena-backend
heroku config:set VERIFY_TOKEN=tu_token_webhook -a serena-backend

# Desplegar backend
cd backend
git init
heroku git:remote -a serena-backend
git add .
git commit -m "Initial deployment"
git push heroku master

# Desplegar frontend
cd ../frontend
git init
heroku git:remote -a serena-frontend
# Ajustar VITE_API_URL para apuntar a serena-backend
echo "VITE_API_URL=https://serena-backend.herokuapp.com/api" > .env
git add .
git commit -m "Initial deployment"
git push heroku master
```

## 10. Checklist Final para Producción

Antes de anunciar el lanzamiento, verifica:

- [ ] Base de datos respaldada y con migración aplicada
- [ ] Certificados SSL instalados y funcionando
- [ ] Firewall configurado correctamente
- [ ] Webhooks de WhatsApp verificados y funcionando
- [ ] Logs rotando correctamente
- [ ] Sistema de monitoreo funcionando
- [ ] Cron jobs para respaldos configurados
- [ ] Contraseñas predeterminadas cambiadas
- [ ] Pruebas de carga básicas realizadas
- [ ] Plan de respaldo y recuperación documentado