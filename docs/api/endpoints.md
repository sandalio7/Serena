# Documentación de Endpoints API

Este documento describe los endpoints disponibles en la API de Serena MVP.

## Base URL

```
https://api.serena-app.com/api  # Producción
http://localhost:5000/api       # Desarrollo
```

## Autenticación

Todos los endpoints, excepto el webhook de WhatsApp y la autenticación, requieren un token JWT válido enviado en el encabezado de autorización:

```
Authorization: Bearer <token>
```

## Formato de Respuesta

Todas las respuestas siguen un formato estándar:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operación completada con éxito"
}
```

En caso de error:

```json
{
  "success": false,
  "error": "Descripción del error",
  "code": 400
}
```

## Endpoints

### Autenticación

#### `POST /api/auth/login`

Inicia sesión y devuelve un token JWT.

**Request Body:**
```json
{
  "email": "ejemplo@correo.com",
  "password": "contraseña123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "first_name": "Usuario",
      "last_name": "Ejemplo",
      "email": "ejemplo@correo.com",
      "role": "familiar"
    }
  },
  "message": "Inicio de sesión exitoso"
}
```

#### `POST /api/auth/refresh`

Renueva un token JWT existente.

**Request Header:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Token renovado"
}
```

### Pacientes

#### `GET /api/patients`

Obtiene la lista de pacientes accesibles para el usuario actual.

**Parámetros de Consulta:**
- `active` (opcional) - Filtrar por estado activo (true/false)
- `limit` (opcional) - Limitar número de resultados (default: 10)
- `offset` (opcional) - Número de resultados a saltar (para paginación)

**Response:**
```json
{
  "success": true,
  "data": {
    "patients": [
      {
        "id": 1,
        "name": "María García",
        "age": 78,
        "conditions": "Alzheimer leve, Hipertensión",
        "active": true
      },
      {
        "id": 2,
        "name": "José Rodríguez",
        "age": 82,
        "conditions": "Parkinson",
        "active": true
      }
    ],
    "total": 2
  },
  "message": "Pacientes recuperados con éxito"
}
```

#### `GET /api/patients/:id`

Obtiene detalles de un paciente específico.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "María García",
    "age": 78,
    "conditions": "Alzheimer leve, Hipertensión",
    "registration_date": "2023-10-15T14:30:00Z",
    "notes": "Prefiere desayunar tarde",
    "active": true,
    "last_update": "2023-11-02T09:45:12Z"
  },
  "message": "Paciente recuperado con éxito"
}
```

#### `POST /api/patients`

Crea un nuevo paciente (solo para usuarios con rol "admin").

**Request Body:**
```json
{
  "name": "Carlos Sánchez",
  "age": 75,
  "conditions": "Diabetes tipo 2, Artritis",
  "notes": "Limitación de movilidad en pierna derecha"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 3,
    "name": "Carlos Sánchez",
    "age": 75,
    "conditions": "Diabetes tipo 2, Artritis",
    "registration_date": "2023-12-01T10:15:30Z",
    "notes": "Limitación de movilidad en pierna derecha",
    "active": true
  },
  "message": "Paciente creado con éxito"
}
```

#### `PUT /api/patients/:id`

Actualiza la información de un paciente.

**Request Body:**
```json
{
  "name": "María García López",
  "age": 79,
  "conditions": "Alzheimer moderado, Hipertensión",
  "notes": "Prefiere desayunar tarde. Alergia a la penicilina."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "María García López",
    "age": 79,
    "conditions": "Alzheimer moderado, Hipertensión",
    "notes": "Prefiere desayunar tarde. Alergia a la penicilina.",
    "active": true,
    "last_update": "2023-12-02T15:30:45Z"
  },
  "message": "Paciente actualizado con éxito"
}
```

#### `DELETE /api/patients/:id`

Desactiva un paciente (no lo elimina de la base de datos).

**Response:**
```json
{
  "success": true,
  "message": "Paciente desactivado con éxito"
}
```

### Cuidadores

#### `GET /api/caregivers`

Obtiene la lista de cuidadores.

**Parámetros de Consulta:**
- `patient_id` (opcional) - Filtrar por paciente
- `active` (opcional) - Filtrar por estado activo (true/false)

**Response:**
```json
{
  "success": true,
  "data": {
    "caregivers": [
      {
        "id": 1,
        "name": "Ana Martínez",
        "phone": "+34612345678",
        "patients": [
          {"id": 1, "name": "María García López"}
        ],
        "active": true
      },
      {
        "id": 2,
        "name": "Luis Fernández",
        "phone": "+34698765432",
        "patients": [
          {"id": 2, "name": "José Rodríguez"}
        ],
        "active": true
      }
    ],
    "total": 2
  },
  "message": "Cuidadores recuperados con éxito"
}
```

#### `GET /api/caregivers/:id`

Obtiene detalles de un cuidador específico.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Ana Martínez",
    "phone": "+34612345678",
    "whatsapp_id": "34612345678",
    "registration_date": "2023-09-20T10:00:00Z",
    "last_activity": "2023-12-03T08:45:12Z",
    "active": true,
    "patients": [
      {"id": 1, "name": "María García López"}
    ]
  },
  "message": "Cuidador recuperado con éxito"
}
```

#### `POST /api/caregivers`

Registra un nuevo cuidador.

**Request Body:**
```json
{
  "name": "Carmen Ruiz",
  "phone": "+34654321789",
  "patients": [1, 3]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 3,
    "name": "Carmen Ruiz",
    "phone": "+34654321789",
    "whatsapp_id": "34654321789",
    "registration_date": "2023-12-03T09:20:15Z",
    "patients": [
      {"id": 1, "name": "María García López"},
      {"id": 3, "name": "Carlos Sánchez"}
    ],
    "active": true
  },
  "message": "Cuidador registrado con éxito"
}
```

#### `PUT /api/caregivers/:id`

Actualiza información de un cuidador.

**Request Body:**
```json
{
  "name": "Ana María Martínez",
  "phone": "+34612345678",
  "patients": [1, 2]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Ana María Martínez",
    "phone": "+34612345678",
    "patients": [
      {"id": 1, "name": "María García López"},
      {"id": 2, "name": "José Rodríguez"}
    ],
    "active": true
  },
  "message": "Cuidador actualizado con éxito"
}
```

#### `DELETE /api/caregivers/:id`

Desactiva un cuidador (no lo elimina de la base de datos).

**Response:**
```json
{
  "success": true,
  "message": "Cuidador desactivado con éxito"
}
```

### Mensajes y Datos Clasificados

#### `GET /api/messages`

Obtiene mensajes enviados por cuidadores.

**Parámetros de Consulta:**
- `patient_id` (requerido) - ID del paciente
- `start_date` (opcional) - Fecha de inicio (formato ISO)
- `end_date` (opcional) - Fecha de fin (formato ISO)
- `limit` (opcional) - Limitar número de resultados (default: 20)
- `offset` (opcional) - Número de resultados a saltar

**Response:**
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "id": 42,
        "caregiver_id": 1,
        "caregiver_name": "Ana Martínez",
        "patient_id": 1,
        "original_text": "Hoy María estuvo un poco mejor. Caminó unos 100 pasos hasta el jardín y comió bien el almuerzo. Sigue olvidando tomar su medicamento para la presión, tuve que recordárselo tres veces. Gastamos 45€ en medicinas.",
        "received_date": "2023-12-01T18:30:45Z",
        "processed": true
      },
      {
        "id": 43,
        "caregiver_id": 1,
        "caregiver_name": "Ana Martínez",
        "patient_id": 1,
        "original_text": "María durmió bien anoche, casi 7 horas seguidas. Desayunó fruta y tostadas, y tomó su medicación sin problemas. Hicimos ejercicios de memoria y recordó los nombres de sus nietos.",
        "received_date": "2023-12-02T09:15:30Z",
        "processed": true
      }
    ],
    "total": 2
  },
  "message": "Mensajes recuperados con éxito"
}
```

#### `GET /api/classified-data`

Obtiene datos clasificados para análisis y visualización.

**Parámetros de Consulta:**
- `patient_id` (requerido) - ID del paciente
- `category` (opcional) - Filtrar por categoría (física, cognitiva, emocional, medicación, gastos)
- `subcategory` (opcional) - Filtrar por subcategoría
- `start_date` (opcional) - Fecha de inicio (formato ISO)
- `end_date` (opcional) - Fecha de fin (formato ISO)
- `grouped` (opcional) - Agrupar por día/semana/mes (default: día)

**Response:**
```json
{
  "success": true,
  "data": {
    "classified_data": [
      {
        "date": "2023-12-01",
        "categories": {
          "Salud Física": {
            "Movilidad": [
              {
                "id": 101,
                "value": "Caminó unos 100 pasos hasta el jardín",
                "confidence": 0.95,
                "message_id": 42
              }
            ],
            "Alimentación": [
              {
                "id": 102,
                "value": "Comió bien el almuerzo",
                "confidence": 0.9,
                "message_id": 42
              }
            ]
          },
          "Medicación": {
            "Adherencia": [
              {
                "id": 103,
                "value": "Sigue olvidando tomar su medicamento para la presión",
                "confidence": 0.98,
                "message_id": 42
              }
            ]
          },
          "Gastos": {
            "Medicamentos": [
              {
                "id": 104,
                "value": "45€",
                "unit": "EUR",
                "confidence": 0.99,
                "message_id": 42
              }
            ]
          }
        }
      },
      {
        "date": "2023-12-02",
        "categories": {
          "Salud Física": {
            "Sueño": [
              {
                "id": 105,
                "value": "Durmió bien, casi 7 horas seguidas",
                "confidence": 0.97,
                "message_id": 43
              }
            ],
            "Alimentación": [
              {
                "id": 106,
                "value": "Desayunó fruta y tostadas",
                "confidence": 0.95,
                "message_id": 43
              }
            ]
          },
          "Salud Cognitiva": {
            "Memoria": [
              {
                "id": 107,
                "value": "Recordó los nombres de sus nietos",
                "confidence": 0.92,
                "message_id": 43
              }
            ]
          },
          "Medicación": {
            "Adherencia": [
              {
                "id": 108,
                "value": "Tomó su medicación sin problemas",
                "confidence": 0.99,
                "message_id": 43
              }
            ]
          }
        }
      }
    ],
    "period": {
      "start": "2023-12-01T00:00:00Z",
      "end": "2023-12-02T23:59:59Z"
    }
  },
  "message": "Datos clasificados recuperados con éxito"
}
```

#### `GET /api/stats/patient/:id`

Obtiene estadísticas resumidas de un paciente.

**Response:**
```json
{
  "success": true,
  "data": {
    "patient_id": 1,
    "patient_name": "María García López",
    "period": {
      "start": "2023-11-01T00:00:00Z",
      "end": "2023-12-03T23:59:59Z"
    },
    "summary": {
      "total_messages": 45,
      "days_with_records": 28,
      "categories_detected": {
        "Salud Física": 40,
        "Salud Cognitiva": 35,
        "Estado Emocional": 30,
        "Medicación": 42,
        "Gastos": 15
      }
    },
    "trends": {
      "Movilidad": "mejora",
      "Alimentación": "estable",
      "Sueño": "deterioro",
      "Memoria": "estable",
      "Humor": "mejora",
      "Adherencia Medicación": "mejora"
    },
    "last_update": "2023-12-03T09:15:30Z"
  },
  "message": "Estadísticas recuperadas con éxito"
}
```

### Webhook para WhatsApp

#### `POST /api/webhook/whatsapp`

Recibe mensajes desde WhatsApp a través de Twilio/MessageBird.

**Request Body (ejemplo de Twilio):**
```json
{
  "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "NumMedia": "0",
  "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "SmsStatus": "received",
  "Body": "Hoy José durmió bien. Desayunó completo y tomó sus medicinas. Lo llevé a caminar al parque y se sintió animado.",
  "To": "whatsapp:+14155238886",
  "NumSegments": "1",
  "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "From": "whatsapp:+34698765432",
  "ApiVersion": "2010-04-01"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Mensaje recibido y procesado"
}
```

#### `GET /api/webhook/whatsapp`

Endpoint de verificación para configuración inicial de webhook.

**Parámetros de Consulta:**
- `hub.mode` - Modo de verificación
- `hub.verify_token` - Token de verificación
- `hub.challenge` - Challenge para responder

**Response:**
El valor del parámetro `hub.challenge` si la verificación es exitosa.

### Usuarios

#### `GET /api/users/me`

Obtiene información del usuario actual.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "ejemplo@correo.com",
    "first_name": "Usuario",
    "last_name": "Ejemplo",
    "role": "familiar",
    "registration_date": "2023-10-01T12:00:00Z",
    "last_access": "2023-12-03T14:25:30Z",
    "patient_access": [
      {"id": 1, "name": "María García López"}
    ]
  },
  "message": "Información de usuario recuperada con éxito"
}
```

#### `PUT /api/users/me`

Actualiza información del usuario actual.

**Request Body:**
```json
{
  "first_name": "Usuario Actualizado",
  "last_name": "Ejemplo Modificado",
  "email": "nuevo.email@correo.com"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "nuevo.email@correo.com",
    "first_name": "Usuario Actualizado",
    "last_name": "Ejemplo Modificado",
    "role": "familiar"
  },
  "message": "Usuario actualizado con éxito"
}
```

#### `PUT /api/users/password`

Actualiza la contraseña del usuario actual.

**Request Body:**
```json
{
  "current_password": "contraseña123",
  "new_password": "nuevaContraseña456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Contraseña actualizada con éxito"
}
```

#### `POST /api/auth/forgot-password`

Solicita un token para restablecer la contraseña.

**Request Body:**
```json
{
  "email": "ejemplo@correo.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Si el email está registrado, recibirás instrucciones para restablecer tu contraseña"
}
```

#### `POST /api/auth/reset-password`

Restablece la contraseña usando un token válido.

**Request Body:**
```json
{
  "token": "reset-token-example",
  "new_password": "nuevaContraseña789"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Contraseña restablecida con éxito"
}
```

### Administración (solo roles admin)

#### `GET /api/admin/users`

Obtiene todos los usuarios del sistema.

**Response:**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "email": "admin@serena.com",
        "first_name": "Admin",
        "last_name": "Serena",
        "role": "admin",
        "active": true
      },
      {
        "id": 2,
        "email": "familiar@ejemplo.com",
        "first_name": "Usuario",
        "last_name": "Familiar",
        "role": "familiar",
        "active": true
      }
    ],
    "total": 2
  },
  "message": "Usuarios recuperados con éxito"
}
```

#### `POST /api/admin/users`

Crea un nuevo usuario.

**Request Body:**
```json
{
  "email": "nuevo@ejemplo.com",
  "first_name": "Nuevo",
  "last_name": "Usuario",
  "password": "contraseña123",
  "role": "familiar",
  "patient_access": [1, 3]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 3,
    "email": "nuevo@ejemplo.com",
    "first_name": "Nuevo",
    "last_name": "Usuario",
    "role": "familiar",
    "active": true
  },
  "message": "Usuario creado con éxito"
}
```

#### `GET /api/admin/stats`

Obtiene estadísticas generales del sistema.

**Response:**
```json
{
  "success": true,
  "data": {
    "patients": {
      "total": 10,
      "active": 8
    },
    "caregivers": {
      "total": 15,
      "active": 12
    },
    "messages": {
      "total": 1250,
      "last_24h": 45,
      "last_7d": 320
    },
    "classified_data": {
      "total": 6500,
      "categories": {
        "Salud Física": 2500,
        "Salud Cognitiva": 1500,
        "Estado Emocional": 1200,
        "Medicación": 800,
        "Gastos": 500
      }
    },
    "users": {
      "total": 30,
      "by_role": {
        "admin": 2,
        "familiar": 20,
        "profesional": 8
      }
    }
  },
  "message": "Estadísticas recuperadas con éxito"
}
```

## Códigos de Error

- `400` - Bad Request: Solicitud mal formada o datos inválidos
- `401` - Unauthorized: Autenticación requerida o token inválido
- `403` - Forbidden: No tiene permisos para acceder al recurso
- `404` - Not Found: Recurso no encontrado
- `409` - Conflict: Conflicto con el estado actual del recurso
- `422` - Unprocessable Entity: Entidad no procesable (validación fallida)
- `500` - Internal Server Error: Error interno del servidor

## Rate Limiting

La API implementa límites de tasa para prevenir abusos:
- 100 peticiones por minuto para endpoints públicos
- 300 peticiones por minuto para endpoints autenticados

Las respuestas incluyen encabezados para seguimiento de límites:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1607458556
```

## Versioning

La versión actual de la API es `v1`, implícita en la ruta base.
Para futuras versiones, la ruta incluirá el número de versión: `/api/v2/...`