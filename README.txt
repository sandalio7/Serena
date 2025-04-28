# Serena: Asistente de Monitoreo para Cuidadores

Serena es una solución digital que facilita el monitoreo y seguimiento del estado de salud y bienestar de adultos dependientes a través de la clasificación automatizada de mensajes informales enviados por cuidadores.

## Visión General

Nuestro sistema utiliza inteligencia artificial para transformar mensajes diarios en datos estructurados que se muestran en un dashboard interactivo, permitiendo un seguimiento eficiente del paciente sin aumentar la carga de trabajo de los cuidadores.

## Características Principales

- **Integración con WhatsApp**: Uso de un canal de comunicación ya familiar para los cuidadores.
- **Procesamiento de lenguaje natural**: Conversión automática de mensajes de texto informal en datos estructurados.
- **Categorización sistemática**: Clasificación de la información en categorías clave como salud física, cognitiva, emocional y gastos.
- **Visualización de datos**: Dashboard intuitivo para ver el estado actual y tendencias históricas.
- **Mínima fricción**: El cuidador solo necesita enviar mensajes informales sin un formato especial o entrenamiento complejo.

## Estructura del Proyecto

```
serena_project/
├── backend/           # API Flask y lógica de negocio
├── frontend/          # Interfaz de usuario en React
├── docker/            # Configuración de Docker
├── docs/              # Documentación
├── scripts/           # Scripts de utilidad
├── .github/           # Configuración CI/CD
├── .gitignore
└── README.md
```

## Requisitos Previos

- Python 3.9 o superior
- Node.js 16 o superior
- pip y npm
- Docker y Docker Compose (opcional, para despliegue)

## Instalación y Configuración

### Método 1: Configuración Manual

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/serena-project.git
   cd serena-project
   ```

2. **Configurar el Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Editar con tus configuraciones
   ```

3. **Inicializar la Base de Datos**:
   ```bash
   mkdir -p instance
   flask db upgrade
   ```

4. **Configurar el Frontend**:
   ```bash
   cd ../frontend
   npm install
   echo "VITE_API_URL=http://localhost:5000/api" > .env
   ```

### Método 2: Usando el Script de Configuración

```bash
./scripts/setup_dev.sh
```

### Método 3: Usando Docker

```bash
./scripts/deploy.sh dev  # Para entorno de desarrollo
./scripts/deploy.sh prod  # Para entorno de producción
```

## Ejecución

### Modo Desarrollo (Manual)

1. **Iniciar el Backend**:
   ```bash
   cd backend
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   flask run
   ```

2. **Iniciar el Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

### Modo Desarrollo (Docker)

```bash
docker-compose -f docker/docker-compose.dev.yml up
```

## Uso

1. **Acceso al Dashboard**:
   - Desarrollo: http://localhost:3000
   - Producción: https://tu-dominio.com

2. **Envío de Mensajes (Cuidadores)**:
   - Enviar mensajes al número de WhatsApp configurado
   - Formato: texto natural describiendo el estado del paciente

3. **Visualización de Datos (Familiares/Profesionales)**:
   - Iniciar sesión en el dashboard
   - Seleccionar paciente para ver su estado actual
   - Explorar tendencias históricas por categoría

## Documentación

Para más información, consultar:

- [Visión General del Sistema](docs/architecture/system_overview.md)
- [Flujo de Datos](docs/architecture/data_flow.md)
- [Esquema de Base de Datos](docs/architecture/database_schema.md)
- [API Endpoints](docs/api/endpoints.md)
- [Guía para Cuidadores](docs/user_guides/caregiver_guide.md)
- [Guía para Familiares](docs/user_guides/family_guide.md)

## Desarrollo

### Pruebas

**Backend**:
```bash
cd backend
pytest
```

**Frontend**:
```bash
cd frontend
npm test
```

### Respaldo de Base de Datos

```bash
./scripts/backup_db.sh
```

## Contribución

1. Crear un fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Hacer commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).

## Contacto

Para más información o soporte, contactar a [tu-email@example.com].