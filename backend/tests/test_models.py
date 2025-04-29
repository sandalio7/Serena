# backend/tests/test_models.py
import pytest
from app.models.patient import Patient
from app.models.caregiver import Caregiver
from app.models.message import Message
from app.models.classified_data import ClassifiedData
from app.extensions import db

def test_patient_model(app):
    """Probar la creación de un paciente"""
    with app.app_context():
        # Crear un nuevo paciente
        patient = Patient(
            name="Nuevo Paciente",
            age=80,
            conditions="Parkinson, Diabetes",
            notes="Notas de prueba"
        )
        patient.save()
        
        # Recuperar y verificar
        saved_patient = Patient.get_by_id(patient.id)
        assert saved_patient is not None
        assert saved_patient.name == "Nuevo Paciente"
        assert saved_patient.age == 80
        assert saved_patient.conditions == "Parkinson, Diabetes"

def test_caregiver_model(app):
    """Probar la creación de un cuidador"""
    with app.app_context():
        # Obtener un paciente existente (creado en conftest.py)
        patient = Patient.query.first()
        
        # Crear un nuevo cuidador
        caregiver = Caregiver(
            name="Nuevo Cuidador",
            phone="+5555555555",
            email="nuevo@example.com",
            role="Familiar",
            patient_id=patient.id
        )
        caregiver.save()
        
        # Recuperar y verificar
        saved_caregiver = Caregiver.get_by_phone("+5555555555")
        assert saved_caregiver is not None
        assert saved_caregiver.name == "Nuevo Cuidador"
        assert saved_caregiver.patient_id == patient.id

def test_message_and_classified_data(app):
    """Probar la creación de un mensaje y sus datos clasificados"""
    with app.app_context():
        # Obtener un cuidador y paciente existente
        caregiver = Caregiver.query.first()
        patient = Patient.query.first()
        
        # Crear un mensaje
        message = Message(
            content="Mensaje de prueba para clasificación",
            whatsapp_message_id="test-message-id-12345",
            caregiver_id=caregiver.id,
            patient_id=patient.id
        )
        message.save()
        
        # Crear datos clasificados
        classified = ClassifiedData(
            raw_data='{"test": "data"}',
            summary="Resumen de prueba",
            physical_health='{"detectada": true, "subcategorias": []}',
            message_id=message.id,
            patient_id=patient.id
        )
        classified.save()
        
        # Verificar la relación
        assert message.classified_data is not None
        assert message.classified_data.summary == "Resumen de prueba"
        
        # Verificar método de acceso
        patient_data = ClassifiedData.get_by_patient(patient.id)
        assert len(patient_data) == 1
        assert patient_data[0].summary == "Resumen de prueba"