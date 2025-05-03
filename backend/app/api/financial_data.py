# backend/app/api/financial_data.py
from flask import Blueprint, jsonify, request
from ..models.classified_data import ClassifiedData
from ..models.patient import Patient
from ..extensions import db
import json
from datetime import datetime, timedelta
from ..models.message import Message

# Crear blueprint para datos financieros
financial_bp = Blueprint('financial', __name__, url_prefix='/api/financial')

@financial_bp.route('/summary', methods=['GET'])
def get_financial_summary():
    """Obtener resumen financiero basado en un período"""
    # Obtener parámetros
    patient_id = request.args.get('patient_id', type=int)
    period = request.args.get('period', 'month')
    
    # Validar paciente
    if not patient_id:
        return jsonify({'error': 'Se requiere ID de paciente'}), 400
    
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    # Calcular fecha de inicio según el período
    today = datetime.now()
    if period == 'day':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'fortnight':
        start_date = today - timedelta(days=15)
    else:  # month
        start_date = today - timedelta(days=30)
    
    # Obtener datos clasificados para el período
    data_query = ClassifiedData.query.filter(
        ClassifiedData.patient_id == patient_id,
        ClassifiedData.created_at >= start_date
    ).all()
    
    # Calcular resumen financiero
    total_income = 0
    total_expenses = 0
    categories = {}
    
    for data in data_query:
        # Procesar gastos
        if data.expenses:
            expenses_dict = json.loads(data.expenses)
            
            # Procesar cada subcategoría encontrada
            for item in expenses_dict:
                category_name = item.get('nombre', 'Otros')
                amount_str = item.get('valor', '0')
                
                # Extraer solo valores numéricos
                import re
                amount_match = re.search(r'(\d+(?:\.\d+)?)', amount_str)
                if amount_match:
                    amount = float(amount_match.group(1))
                else:
                    continue
                
                # Agrupar por categoría
                if category_name in categories:
                    categories[category_name]['amount'] += amount
                else:
                    # Asignar un color según la categoría
                    color = get_category_color(category_name)
                    categories[category_name] = {
                        'name': category_name,
                        'amount': amount,
                        'color': color
                    }
                
                total_expenses += amount
    
    # Transformar categorías a lista para el frontend
    categories_list = list(categories.values())
    
    # Resultado
    result = {
        'income': total_income,  # Por ahora solo tenemos gastos
        'expenses': total_expenses,
        'categories': categories_list,
        'period': period
    }
    
    return jsonify(result)

@financial_bp.route('/expenses/categories', methods=['GET'])
def get_expenses_by_category():
    """Obtener gastos agrupados por categoría para un período"""
    # Obtener parámetros
    patient_id = request.args.get('patient_id', type=int)
    period = request.args.get('period', 'month')
    
    # Validar paciente
    if not patient_id:
        return jsonify({'error': 'Se requiere ID de paciente'}), 400
    
    # Calcular fecha de inicio según el período
    today = datetime.now()
    if period == 'day':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'fortnight':
        start_date = today - timedelta(days=15)
    else:  # month
        start_date = today - timedelta(days=30)
    
    # Obtener datos clasificados para el período
    data_query = ClassifiedData.query.filter(
        ClassifiedData.patient_id == patient_id,
        ClassifiedData.created_at >= start_date
    ).all()
    
    # Calcular categorías
    categories = {}
    
    for data in data_query:
        # Procesar gastos
        if data.expenses:
            expenses_dict = json.loads(data.expenses)
            
            # Procesar cada subcategoría encontrada
            for item in expenses_dict:
                category_name = item.get('nombre', 'Otros')
                amount_str = item.get('valor', '0')
                
                # Extraer solo valores numéricos
                import re
                amount_match = re.search(r'(\d+(?:\.\d+)?)', amount_str)
                if amount_match:
                    amount = float(amount_match.group(1))
                else:
                    continue
                
                # Agrupar por categoría
                if category_name in categories:
                    categories[category_name]['amount'] += amount
                else:
                    # Asignar un color según la categoría
                    color = get_category_color(category_name)
                    categories[category_name] = {
                        'name': category_name,
                        'amount': amount,
                        'color': color
                    }
    
    # Transformar categorías a lista para el frontend
    categories_list = list(categories.values())
    
    return jsonify(categories_list)

@financial_bp.route('/transactions', methods=['POST'])
def register_transaction():
    """Registrar una nueva transacción financiera"""
    # Obtener datos de la solicitud
    data = request.json
    
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400
    
    # Validar datos requeridos
    required_fields = ['patient_id', 'type', 'category', 'amount', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Falta el campo requerido: {field}'}), 400
    
    patient_id = data['patient_id']
    
    # Validar paciente
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    # Crear estructura para la nueva transacción
    transaction_type = data['type']  # 'income' o 'expense'
    category = data['category']
    amount = float(data['amount'])
    transaction_date = data['date']
    
    # Crear nueva entrada de ClassifiedData
    import datetime
    
    # Crear mensaje artificial
    message_text = f"Registro manual: {transaction_type} de ${amount} en categoría {category} del {transaction_date}"
    message = Message(
        content=message_text,
        caregiver_id=1,  # ID por defecto
        patient_id=patient_id,
        created_at=datetime.datetime.strptime(transaction_date, '%Y-%m-%d')
    )
    db.session.add(message)
    db.session.commit()
    
    # Crear estructura de datos clasificados
    expenses_data = []
    if transaction_type == 'expense':
        expenses_data = [{
            'nombre': category,
            'valor': str(amount),
            'confianza': 1.0
        }]
    
    # Guardar datos clasificados
    classified_data = ClassifiedData(
        raw_data=json.dumps({"manual_entry": True}),
        expenses=json.dumps(expenses_data),
        summary=f"Registro manual: {transaction_type} de ${amount} en {category}",
        message_id=message.id,
        patient_id=patient_id,
        created_at=datetime.datetime.strptime(transaction_date, '%Y-%m-%d')
    )
    
    db.session.add(classified_data)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Transacción registrada correctamente',
        'transaction': {
            'type': transaction_type,
            'category': category,
            'amount': amount,
            'date': transaction_date
        }
    })

def get_category_color(category):
    """Asignar un color a cada categoría"""
    color_map = {
        'Vivienda': '#1e40af',
        'Servicios básicos': '#3b82f6',
        'Cuidados': '#ef4444',
        'Salud': '#f97316',
        'Supermercado': '#22c55e',
        'Transporte': '#a855f7',
        'Medicamentos': '#06b6d4',
        'Recreación': '#f59e0b',
        'Varios': '#6b7280',
        'Otros': '#6b7280'
    }
    
    # Devolver color para la categoría o uno por defecto
    return color_map.get(category, '#6b7280')  # Gris por defecto