# Visión General del Sistema Serena

## Introducción

Serena es una solución digital diseñada para facilitar el monitoreo y seguimiento del estado de salud y bienestar de adultos dependientes. El sistema utiliza inteligencia artificial para transformar mensajes informales enviados por cuidadores en datos estructurados que se visualizan en un dashboard interactivo, permitiendo un seguimiento eficiente sin aumentar la carga de trabajo de los cuidadores.

## Arquitectura General

La arquitectura de Serena MVP se basa en cinco componentes principales interconectados:

1. **Canal de mensajería (WhatsApp)** - Para la interacción con cuidadores
2. **Backend (Flask)** - Para procesamiento y API
3. **Servicio de IA (Google Gemini)** - Para clasificación de mensajes
4. **Base de datos (MongoDB)** - Para almacenamiento
5. **Frontend (React.js)** - Para visualización de dashboard

![Arquitectura de Serena MVP](https://placeholder-image.com/architecture)

## Flujo de Datos Principal

1. **Entrada de Mensaje**:
   ```
   Cuidador → WhatsApp → Twilio/MessageBird → Webhook → Backend Flask
   ```

2. **Procesamiento**:
   ```
   Backend Flask → Google Gemini API → Clasificación → MongoDB
   ```

3. **Consulta de Dashboard**:
   ```
   Frontend React → Petición API → Backend Flask → Consulta MongoDB → Respuesta → Frontend
   ```

## Componentes Clave

### Backend (Flask)
- Implementa la API REST para el frontend
- Procesa webhooks de WhatsApp
- Interactúa con la API de Google Gemini para la clasificación
- Gestiona la autenticación y autorización
- Almacena y recupera datos de MongoDB

### Frontend (React)
- Proporciona una interfaz de usuario responsive
- Visualiza datos de pacientes en un dashboard
- Muestra tendencias y patrones en los datos
- Permite la gestión de pacientes y cuidadores
- Implementa filtros y vistas personalizadas

### Servicio de IA (Google Gemini)
- Clasifica los mensajes de texto en categorías estructuradas
- Extrae información relevante sobre el estado del paciente
- Proporciona un resumen del estado general

### Base de Datos (MongoDB)
- Almacena información de pacientes y cuidadores
- Guarda mensajes originales y datos clasificados
- Permite consultas eficientes para el dashboard

### Sistema de Mensajería (WhatsApp)
- Proporciona un canal familiar para los cuidadores
- Envía mensajes al sistema a través de webhooks
- Opcionalmente, envía confirmaciones a los cuidadores

## Seguridad e Integridad

El sistema implementa las siguientes medidas de seguridad:
- HTTPS para todas las comunicaciones
- Tokens JWT para autenticación
- Acceso basado en roles
- Sanitización de inputs
- Variables de entorno para secretos