# backend/app/utils/db_init.py
import os
from flask import Flask
from ..extensions import db
from ..models.patient import Patient
from ..models.caregiver import Caregiver
from ..models.message import Message
from ..models.classified_data import ClassifiedData
from ..config import Config

def init_db():
    """Inicializar la base de datos con las tablas necesarias"""
    # Crear una mini aplicación para el contexto
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Asegurarnos de que el directorio instance existe
    os.makedirs('instance', exist_ok=True)
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Crear todas las tablas definidas en los modelos
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente.")
        
        # Crear datos de prueba
        create_test_data(db)

def create_test_data(db):
    """Crear datos de prueba para desarrollo"""
    # Verificar si ya hay datos
    if Patient.query.first() is not None:
        print("Ya existen datos de prueba. Omitiendo creación.")
        return

    # Crear un paciente de prueba
    patient = Patient(name="María García", age=78, conditions="Alzheimer inicial, hipertensión")
    db.session.add(patient)
    
    # Crear cuidadores
    caregiver1 = Caregiver(
        name="Ana Pérez", 
        phone="+1234567890",  # Número ficticio
        email="ana@example.com", 
        role="Profesional",
        patient=patient
    )
    
    caregiver2 = Caregiver(
        name="Juan Rodríguez", 
        phone="+0987654321",  # Número ficticio
        email="juan@example.com", 
        role="Familiar",
        patient=patient
    )
    
    db.session.add_all([caregiver1, caregiver2])
    db.session.commit()
    
    print("Datos de prueba creados: 1 paciente y 2 cuidadores")

if __name__ == "__main__":
    init_db()