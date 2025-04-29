# backend/tests/conftest.py
import os
import pytest
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.patient import Patient
from app.models.caregiver import Caregiver
from app.models.message import Message
from app.models.classified_data import ClassifiedData

@pytest.fixture
def app():
    """Crear y configurar una instancia de Flask para testing"""
    app = create_app('testing')
    
    # Crear el contexto de aplicación
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Insertar datos de prueba
        create_test_data()
        
        yield app
        
        # Limpiar después de las pruebas
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Un cliente de prueba para la aplicación"""
    return app.test_client()

def create_test_data():
    """Crear datos de prueba para los tests"""
    # Crear un paciente de prueba
    patient = Patient(name="Test Patient", age=75, conditions="Test Condition")
    db.session.add(patient)
    db.session.flush()
    
    # Crear un cuidador de prueba
    caregiver = Caregiver(
        name="Test Caregiver", 
        phone="+1234567890",
        email="test@example.com",
        role="Profesional",
        patient_id=patient.id
    )
    db.session.add(caregiver)
    
    db.session.commit()
    
    return patient, caregiver