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

@patient_bp.route('/<int:patient_id>/financial/summary', methods=['GET'])
def get_financial_summary(patient_id):
    """Obtener resumen financiero de un paciente"""
    # Verificar si el paciente existe
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    period = request.args.get('period', 'month')  # day, week, fortnight, month
    
    # Obtener datos clasificados con gastos
    classified_data = ClassifiedData.get_by_patient(patient_id)
    
    # Filtrar por período (implementar filtrado por fecha aquí)
    total_income = 0
    total_expenses = 0
    expense_categories = {}
    
    for data in classified_data:
        # Procesar gastos
        if data.expenses_dict:
            for category, items in data.expenses_dict.items():
                if isinstance(items, list):
                    for item in items:
                        if item.get('amount'):
                            amount = float(item.get('amount', 0))
                            total_expenses += amount
                            if category not in expense_categories:
                                expense_categories[category] = 0
                            expense_categories[category] += amount
        
        # Procesar ingresos (si los tienes en los datos)
        # Aquí puedes agregar la lógica para procesar ingresos
    
    # Formatear categorías para el frontend
    categories = []
    colors = ['#1e40af', '#3b82f6', '#ef4444', '#f97316', '#22c55e', '#a855f7', '#6b7280']
    
    for i, (category, amount) in enumerate(expense_categories.items()):
        categories.append({
            'name': category,
            'amount': amount,
            'color': colors[i % len(colors)]
        })
    
    result = {
        'income': total_income,
        'expenses': total_expenses,
        'categories': categories
    }
    
    return jsonify(result)

@patient_bp.route('/<int:patient_id>/financial/expenses-by-category', methods=['GET'])
def get_expenses_by_category(patient_id):
    """Obtener gastos por categoría"""
    # Verificar si el paciente existe
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    period = request.args.get('period', 'month')
    
    # Obtener datos clasificados con gastos
    classified_data = ClassifiedData.get_by_patient(patient_id)
    
    expense_categories = {}
    
    for data in classified_data:
        if data.expenses_dict:
            for category, items in data.expenses_dict.items():
                if isinstance(items, list):
                    for item in items:
                        if item.get('amount'):
                            amount = float(item.get('amount', 0))
                            if category not in expense_categories:
                                expense_categories[category] = 0
                            expense_categories[category] += amount
    
    # Formatear para el frontend
    colors = ['#1e40af', '#3b82f6', '#ef4444', '#f97316', '#22c55e', '#a855f7', '#6b7280']
    result = []
    
    for i, (category, amount) in enumerate(expense_categories.items()):
        result.append({
            'name': category,
            'amount': amount,
            'color': colors[i % len(colors)]
        })
    
    return jsonify(result)