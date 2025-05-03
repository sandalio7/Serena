# backend/app/api/patient_data.py
from flask import Blueprint, jsonify, request
from ..models.patient import Patient
from ..models.classified_data import ClassifiedData

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/', methods=['GET'])
def get_patients():
    """Obtener lista de pacientes"""
    patients = Patient.get_all()
    result = [{
        'id': p.id,
        'name': p.name,
        'age': p.age,
        'conditions': p.conditions,
        'created_at': p.created_at.isoformat()
    } for p in patients]
    
    return jsonify(result)

@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Obtener detalles de un paciente por ID"""
    patient = Patient.get_by_id(patient_id)
    
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    # Datos básicos del paciente
    result = {
        'id': patient.id,
        'name': patient.name,
        'age': patient.age,
        'conditions': patient.conditions,
        'notes': patient.notes,
        'created_at': patient.created_at.isoformat(),
        'updated_at': patient.updated_at.isoformat()
    }
    
    return jsonify(result)

@patient_bp.route('/list', methods=['GET'])
def get_patients_list():
    """Obtener lista simplificada de pacientes para selección"""
    patients = Patient.get_all()
    result = [{
        'id': p.id,
        'name': p.name
    } for p in patients]
    
    return jsonify(result)

@patient_bp.route('/<int:patient_id>/data', methods=['GET'])
def get_patient_data(patient_id):
    """Obtener datos clasificados de un paciente"""
    # Verificar si el paciente existe
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    # Obtener datos clasificados
    classified_data = ClassifiedData.get_by_patient(patient_id)
    
    # Transformar datos para respuesta API
    result = [{
        'id': data.id,
        'created_at': data.created_at.isoformat(),
        'summary': data.summary,
        'physical_health': data.physical_health_dict,
        'cognitive_health': data.cognitive_health_dict,
        'emotional_state': data.emotional_state_dict,
        'medication': data.medication_dict,
        'expenses': data.expenses_dict
    } for data in classified_data]
    
    return jsonify(result)