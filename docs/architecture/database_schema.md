# Esquema de la Base de Datos Serena

Este documento describe el esquema de la base de datos MongoDB utilizada en el MVP de Serena.

## Colecciones

El sistema utiliza cinco colecciones principales:

1. **Pacientes** - Información sobre los pacientes monitoreados
2. **Cuidadores** - Información sobre los cuidadores que envían reportes
3. **Mensajes** - Mensajes originales recibidos vía WhatsApp
4. **DatosClasificados** - Datos estructurados extraídos de los mensajes
5. **Usuarios** - Cuentas de usuarios del sistema (familiares, profesionales)

## Diagrama de Relaciones

```
+------------+       +-------------+       +----------+
|  Pacientes |<----->| Cuidadores  |------>| Mensajes |
+------------+       +-------------+       +----------+
      ^                    ^                    |
      |                    |                    |
      |                    |                    v
+----------+               |            +-----------------+
| Usuarios |---------------+            | DatosClasificados |
+----------+                           +-----------------+
```

## Estructura de Colecciones

### Colección: Pacientes

```json
{
  "_id": "ObjectId",
  "nombre": "String",
  "edad": "Number",
  "condiciones": ["String"],
  "fecha_registro": "Date",
  "notas": "String",
  "activo": "Boolean",
  "ultima_actualizacion": "Date"
}
```

### Colección: Cuidadores

```json
{
  "_id": "ObjectId",
  "nombre": "String",
  "telefono": "String",
  "whatsapp_id": "String",
  "pacientes": ["ObjectId"],  // Referencias a pacientes
  "fecha_registro": "Date",
  "ultima_actividad": "Date",
  "activo": "Boolean"
}
```

### Colección: Mensajes

```json
{
  "_id": "ObjectId",
  "cuidador_id": "ObjectId",  // Referencia al cuidador
  "paciente_id": "ObjectId",  // Referencia al paciente
  "texto_original": "String",
  "fecha_recibido": "Date",
  "procesado": "Boolean",
  "fecha_procesado": "Date",
  "error_procesamiento": "String"
}
```

### Colección: DatosClasificados

```json
{
  "_id": "ObjectId",
  "mensaje_id": "ObjectId",  // Referencia al mensaje original
  "paciente_id": "ObjectId", // Referencia al paciente
  "categoria": "String",     // Ej: "Salud Física"
  "subcategoria": "String",  // Ej: "Movilidad"
  "valor": "Mixed",          // Puede ser String, Number, Boolean
  "valor_texto": "String",   // Texto extraído del mensaje
  "unidad": "String",        // Opcional, ej: "pasos", "horas"
  "confianza": "Number",     // Entre 0 y 1
  "fecha_dato": "Date"       // Fecha a la que se refiere el dato
}
```

### Colección: Usuarios

```json
{
  "_id": "ObjectId",
  "email": "String",
  "password_hash": "String",
  "nombre": "String",
  "apellido": "String",
  "rol": "String",           // "familiar", "profesional", "admin"
  "pacientes_acceso": ["ObjectId"], // Pacientes a los que tiene acceso
  "fecha_registro": "Date",
  "ultimo_acceso": "Date",
  "activo": "Boolean",
  "token_reset": "String",
  "token_expira": "Date"
}
```

## Índices

### Índices Primarios

- `pacientes`: Índice único en `_id`
- `cuidadores`: Índice único en `_id`
- `mensajes`: Índice único en `_id`
- `datos_clasificados`: Índice único en `_id`
- `usuarios`: Índice único en `_id`

### Índices Secundarios

- `cuidadores`: Índice único en `whatsapp_id`
- `usuarios`: Índice único en `email`
- `mensajes`: Índice compuesto en `(paciente_id, fecha_recibido)`
- `datos_clasificados`: Índice compuesto en `(paciente_id, categoria, fecha_dato)`

## Relaciones

1. **Pacientes - Cuidadores**: Relación muchos a muchos
   - Un paciente puede tener varios cuidadores
   - Un cuidador puede atender a varios pacientes
   - Implementado con array de referencias en `cuidadores.pacientes`

2. **Cuidadores - Mensajes**: Relación uno a muchos
   - Un cuidador envía muchos mensajes
   - Implementado con referencia en `mensajes.cuidador_id`

3. **Pacientes - Mensajes**: Relación uno a muchos
   - Un paciente tiene muchos mensajes asociados
   - Implementado con referencia en `mensajes.paciente_id`

4. **Mensajes - DatosClasificados**: Relación uno a muchos
   - Un mensaje genera múltiples datos clasificados
   - Implementado con referencia en `datos_clasificados.mensaje_id`

5. **Pacientes - DatosClasificados**: Relación uno a muchos
   - Un paciente tiene muchos datos clasificados
   - Implementado con referencia en `datos_clasificados.paciente_id`

6. **Usuarios - Pacientes**: Relación muchos a muchos
   - Un usuario puede acceder a varios pacientes
   - Un paciente puede ser accedido por varios usuarios
   - Implementado con array de referencias en `usuarios.pacientes_acceso`

## Consideraciones de Escalabilidad

1. **Particionamiento (Sharding)**:
   - La colección `datos_clasificados` será la que más crezca
   - Clave de partición recomendada: `paciente_id`

2. **TTL (Time-To-Live)**:
   - Considerar TTL para logs detallados o datos temporales

3. **Migración Futura**:
   - Diseño compatible con migración a PostgreSQL si se requiere
   - Relaciones definidas con IDs claros para facilitar migración