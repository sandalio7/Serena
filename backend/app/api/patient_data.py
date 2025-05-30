# backend/app/api/patient_data.py
from flask import Blueprint, jsonify, request
from ..models.patient import Patient
from ..models.message import Message
from ..models.category import Category
from ..models.subcategory import Subcategory
from ..models.classified_value import ClassifiedValue
from ..extensions import db
from datetime import datetime, timedelta

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
    """Obtener datos clasificados de un paciente usando la nueva estructura"""
    # Verificar si el paciente existe
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    # Obtener parámetros opcionales
    days = request.args.get('days', default=30, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    # Obtener valores clasificados del paciente
    values = ClassifiedValue.query.join(
        Message, ClassifiedValue.message_id == Message.id
    ).join(
        Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
    ).join(
        Category, Subcategory.category_id == Category.id
    ).filter(
        Message.patient_id == patient_id,
        Message.created_at >= start_date
    ).order_by(Message.created_at.desc()).all()
    
    # Agrupar datos por categoría para mantener compatibilidad
    categorized_data = {
        'physical_health': [],
        'cognitive_health': [],
        'emotional_state': [],
        'medication': [],
        'expenses': []
    }
    
    category_mapping = {
        'Salud Física': 'physical_health',
        'Salud Cognitiva': 'cognitive_health',
        'Estado Emocional': 'emotional_state',
        'Medicación': 'medication',
        'Gastos': 'expenses'
    }
    
    for value in values:
        category_name = value.subcategory.category.name
        api_category = category_mapping.get(category_name)
        
        if api_category:
            categorized_data[api_category].append({
                'id': value.id,
                'subcategory': value.subcategory.name,
                'value': value.value,
                'confidence': value.confidence,
                'created_at': value.created_at.isoformat(),
                'message_id': value.message_id
            })
    
    # Transformar datos para mantener compatibilidad con la API anterior
    result = [{
        'id': f"aggregated_{patient_id}",
        'created_at': datetime.now().isoformat(),
        'summary': f"Datos agregados de los últimos {days} días",
        'physical_health': categorized_data['physical_health'],
        'cognitive_health': categorized_data['cognitive_health'],
        'emotional_state': categorized_data['emotional_state'],
        'medication': categorized_data['medication'],
        'expenses': categorized_data['expenses']
    }]
    
    return jsonify(result)

@patient_bp.route('/<int:patient_id>/financial/summary', methods=['GET'])
def get_financial_summary(patient_id):
    """Obtener resumen financiero de un paciente usando la nueva estructura"""
    # Verificar si el paciente existe
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    period = request.args.get('period', 'month')  # day, week, fortnight, month
    
    # Calcular fecha de inicio según período
    today = datetime.now()
    if period == 'day':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'fortnight':
        start_date = today - timedelta(days=15)
    else:  # month
        start_date = today - timedelta(days=30)
    
    # Buscar categoría de Gastos
    expenses_category = Category.query.filter(Category.name == 'Gastos').first()
    
    total_income = 0
    total_expenses = 0
    expense_categories = {}
    
    if expenses_category:
        # Obtener subcategorías de gastos
        expense_subcategories = Subcategory.query.filter(Subcategory.category_id == expenses_category.id).all()
        subcategory_ids = [subcat.id for subcat in expense_subcategories]
        
        # Obtener valores clasificados para gastos en el período
        expense_values = ClassifiedValue.query.join(
            Message, ClassifiedValue.message_id == Message.id
        ).filter(
            ClassifiedValue.subcategory_id.in_(subcategory_ids),
            Message.patient_id == patient_id,
            Message.created_at >= start_date
        ).all()
        
        # Procesar cada valor de gasto
        for value in expense_values:
            subcategory = Subcategory.query.get(value.subcategory_id)
            subcategory_name = subcategory.name
            
            # Extraer monto del valor
            import re
            amount_match = re.search(r'(\d+(?:\.\d+)?)', value.value)
            if amount_match:
                amount = float(amount_match.group(1))
                total_expenses += amount
                
                if subcategory_name not in expense_categories:
                    expense_categories[subcategory_name] = 0
                expense_categories[subcategory_name] += amount
    
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
    """Obtener gastos por categoría usando la nueva estructura"""
    # Verificar si el paciente existe
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    period = request.args.get('period', 'month')
    
    # Calcular fecha de inicio según período
    today = datetime.now()
    if period == 'day':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'fortnight':
        start_date = today - timedelta(days=15)
    else:  # month
        start_date = today - timedelta(days=30)
    
    # Buscar categoría de Gastos
    expenses_category = Category.query.filter(Category.name == 'Gastos').first()
    
    expense_categories = {}
    
    if expenses_category:
        # Obtener subcategorías de gastos
        expense_subcategories = Subcategory.query.filter(Subcategory.category_id == expenses_category.id).all()
        subcategory_ids = [subcat.id for subcat in expense_subcategories]
        
        # Obtener valores clasificados para gastos en el período
        expense_values = ClassifiedValue.query.join(
            Message, ClassifiedValue.message_id == Message.id
        ).filter(
            ClassifiedValue.subcategory_id.in_(subcategory_ids),
            Message.patient_id == patient_id,
            Message.created_at >= start_date
        ).all()
        
        # Procesar cada valor de gasto
        for value in expense_values:
            subcategory = Subcategory.query.get(value.subcategory_id)
            subcategory_name = subcategory.name
            
            # Extraer monto del valor
            import re
            amount_match = re.search(r'(\d+(?:\.\d+)?)', value.value)
            if amount_match:
                amount = float(amount_match.group(1))
                
                if subcategory_name not in expense_categories:
                    expense_categories[subcategory_name] = 0
                expense_categories[subcategory_name] += amount
    
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