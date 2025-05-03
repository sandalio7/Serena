import sqlite3

# Conectar a la base de datos - usando una ruta relativa desde la carpeta backend
conn = sqlite3.connect('instance/serena.db')
cursor = conn.cursor()

# Mostrar datos actuales
print("Datos actuales:")
cursor.execute("SELECT id, name, phone FROM caregivers")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Nombre: {row[1]}, Teléfono: {row[2]}")

# Actualizar el número de teléfono
nuevo_telefono = '+5493815122808'  # Reemplaza esto con tu número de WhatsApp real
id_cuidador = 1  # ID del cuidador a actualizar (Ana Pérez en tu caso)

print(f"\nActualizando número de teléfono del cuidador con ID {id_cuidador} a {nuevo_telefono}...")
cursor.execute("UPDATE caregivers SET phone = ? WHERE id = ?", 
               (nuevo_telefono, id_cuidador))

# Verificar el cambio
print("\nDatos después de la actualización:")
cursor.execute("SELECT id, name, phone FROM caregivers")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Nombre: {row[1]}, Teléfono: {row[2]}")

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("\nNúmero de teléfono actualizado correctamente.")