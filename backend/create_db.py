# backend/create_db.py
import os
import sqlite3
from pathlib import Path

# Ruta al directorio actual
current_dir = Path(__file__).parent.absolute()

# Asegurarnos de que existe el directorio instance
instance_dir = current_dir / "instance"
instance_dir.mkdir(exist_ok=True)

# Ruta completa al archivo de base de datos
db_path = instance_dir / "serena.db"

print(f"Creando base de datos en: {db_path}")

# Crear la base de datos y tablas básicas
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tablas
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    conditions TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS caregivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE,
    email TEXT,
    role TEXT,
    patient_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    whatsapp_message_id TEXT UNIQUE,
    caregiver_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (caregiver_id) REFERENCES caregivers (id),
    FOREIGN KEY (patient_id) REFERENCES patients (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS classified_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_data TEXT NOT NULL,
    physical_health TEXT,
    cognitive_health TEXT,
    emotional_state TEXT,
    medication TEXT,
    expenses TEXT,
    summary TEXT,
    message_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES messages (id),
    FOREIGN KEY (patient_id) REFERENCES patients (id)
)
''')

# Verificar si ya hay datos
cursor.execute("SELECT COUNT(*) FROM patients")
patient_count = cursor.fetchone()[0]

# Crear datos de prueba solo si no hay pacientes
if patient_count == 0:
    # Insertar un paciente de prueba
    cursor.execute('''
    INSERT INTO patients (name, age, conditions)
    VALUES (?, ?, ?)
    ''', ("María García", 78, "Alzheimer inicial, hipertensión"))
    
    # Obtener el ID del paciente
    patient_id = cursor.lastrowid
    
    # Insertar cuidadores
    cursor.execute('''
    INSERT INTO caregivers (name, phone, email, role, patient_id)
    VALUES (?, ?, ?, ?, ?)
    ''', ("Ana Pérez", "+1234567890", "ana@example.com", "Profesional", patient_id))
    
    cursor.execute('''
    INSERT INTO caregivers (name, phone, email, role, patient_id)
    VALUES (?, ?, ?, ?, ?)
    ''', ("Juan Rodríguez", "+0987654321", "juan@example.com", "Familiar", patient_id))
    
    print("Datos de prueba creados: 1 paciente y 2 cuidadores")
else:
    print(f"Ya existen {patient_count} pacientes en la base de datos. Omitiendo creación de datos de prueba.")

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos inicializada correctamente.")