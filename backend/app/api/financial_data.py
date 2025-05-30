# backend/app/api/financial_data.py
from flask import Blueprint, jsonify, request
from ..models.patient import Patient
from ..models.message import Message
from ..models.category import Category
from ..models.subcategory import Subcategory
from ..models.classified_value import ClassifiedValue
from ..extensions import db
import json
from datetime import datetime, timedelta

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
    
    # Obtener datos de gastos usando solo la estructura normalizada
    total_income = 0
    total_expenses = 0
    categories = {}
    
    # Buscar categoría de Gastos
    expenses_category = Category.query.filter(Category.name == 'Gastos').first()
    
    if expenses_category:
        # Obtener todas las subcategorías de gastos
        expense_subcategories = Subcategory.query.filter(Subcategory.category_id == expenses_category.id).all()
        subcategory_ids = [subcat.id for subcat in expense_subcategories]
        
        # Obtener valores clasificados para gastos
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
            amount_str = value.value
            
            # Extraer solo valores numéricos
            import re
            amount_match = re.search(r'(\d+(?:\.\d+)?)', amount_str)
            if amount_match:
                amount = float(amount_match.group(1))
            else:
                continue
            
            # Agrupar por categoría
            if subcategory_name in categories:
                categories[subcategory_name]['amount'] += amount
            else:
                # Asignar un color según la categoría
                color = get_category_color(subcategory_name)
                categories[subcategory_name] = {
                    'name': subcategory_name,
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
    
    # Obtener datos de gastos usando solo la estructura normalizada
    categories = {}
    
    # Buscar categoría de Gastos
    expenses_category = Category.query.filter(Category.name == 'Gastos').first()
    
    if expenses_category:
        # Obtener todas las subcategorías de gastos
        expense_subcategories = Subcategory.query.filter(Subcategory.category_id == expenses_category.id).all()
        subcategory_ids = [subcat.id for subcat in expense_subcategories]
        
        # Obtener valores clasificados para gastos
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
            amount_str = value.value
            
            # Extraer solo valores numéricos
            import re
            amount_match = re.search(r'(\d+(?:\.\d+)?)', amount_str)
            if amount_match:
                amount = float(amount_match.group(1))
            else:
                continue
            
            # Agrupar por categoría
            if subcategory_name in categories:
                categories[subcategory_name]['amount'] += amount
            else:
                # Asignar un color según la categoría
                color = get_category_color(subcategory_name)
                categories[subcategory_name] = {
                    'name': subcategory_name,
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
    category_name = data['category']
    amount = float(data['amount'])
    transaction_date = data['date']
    
    # Crear nuevo mensaje artificial
    import datetime
    
    message_text = f"Registro manual: {transaction_type} de ${amount} en categoría {category_name} del {transaction_date}"
    message = Message(
        content=message_text,
        caregiver_id=1,  # ID por defecto
        patient_id=patient_id,
        created_at=datetime.datetime.strptime(transaction_date, '%Y-%m-%d')
    )
    db.session.add(message)
    db.session.commit()
    
    # Guardar en la estructura normalizada
    if transaction_type == 'expense':
        # Buscar categoría de gastos
        expenses_category = Category.query.filter(Category.name == 'Gastos').first()
        
        if expenses_category:
            # Buscar la subcategoría correspondiente
            subcategory = Subcategory.query.filter(
                Subcategory.category_id == expenses_category.id,
                Subcategory.name == category_name
            ).first()
            
            # Si no existe la subcategoría, usar "Otros"
            if not subcategory:
                subcategory = Subcategory.query.filter(
                    Subcategory.category_id == expenses_category.id,
                    Subcategory.name == 'Otros'
                ).first()
            
            if subcategory:
                # Crear valor clasificado
                classified_value = ClassifiedValue(
                    message_id=message.id,
                    subcategory_id=subcategory.id,
                    value=f"${amount}",
                    confidence=1.0
                )
                db.session.add(classified_value)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Transacción registrada correctamente',
        'transaction': {
            'type': transaction_type,
            'category': category_name,
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

@financial_bp.route('/messages-history', methods=['GET'])
def get_messages_history():
    """Obtener historial de mensajes con gastos"""
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
    
    # Obtener datos de gastos usando solo la estructura normalizada
    result = []
    
    # Buscar categoría de Gastos
    expenses_category = Category.query.filter(Category.name == 'Gastos').first()
    
    if expenses_category:
        # Obtener todas las subcategorías de gastos
        expense_subcategories = Subcategory.query.filter(Subcategory.category_id == expenses_category.id).all()
        subcategory_ids = [subcat.id for subcat in expense_subcategories]
        
        # Obtener valores clasificados para gastos
        expense_values = ClassifiedValue.query.join(
            Message, ClassifiedValue.message_id == Message.id
        ).join(
            Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
        ).filter(
            ClassifiedValue.subcategory_id.in_(subcategory_ids),
            Message.patient_id == patient_id,
            Message.created_at >= start_date
        ).order_by(Message.created_at.desc()).all()
        
        # Procesar cada valor de gasto
        for value in expense_values:
            message = Message.query.get(value.message_id)
            subcategory = Subcategory.query.get(value.subcategory_id)
            
            # Extraer monto del valor
            amount_str = value.value
            
            # Extraer solo valores numéricos
            import re
            amount_match = re.search(r'(\d+(?:\.\d+)?)', amount_str)
            if amount_match:
                amount = float(amount_match.group(1))
            else:
                continue
            
            # Determinar si fue editado (basado en contenido del mensaje)
            is_edited = 'Registro manual' in message.content or 'editado' in message.content.lower()
            
            # Añadir a resultados
            result.append({
                'id': value.id,  # ID de ClassifiedValue para editar/eliminar
                'category': {
                    'name': subcategory.name,
                    'color': get_category_color(subcategory.name)
                },
                'amount': amount,
                'date': value.created_at.isoformat(),
                'message': message.content,
                'message_id': message.id,
                'edited': is_edited
            })
    
    return jsonify(result)

@financial_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """Actualizar una transacción existente"""
    # Obtener datos de la solicitud
    data = request.json
    
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400
    
    # Buscar la transacción en la estructura normalizada
    classified_value = ClassifiedValue.query.get(transaction_id)
    
    if not classified_value:
        return jsonify({'error': 'Transacción no encontrada'}), 404
    
    # Obtener el mensaje asociado
    message = Message.query.get(classified_value.message_id)
    
    if not message:
        return jsonify({'error': 'Mensaje asociado no encontrado'}), 404
    
    # Actualizar campos
    try:
        # Actualizar descripción si se proporcionó
        if 'description' in data:
            message.content = data['description']
        
        # Actualizar monto si se proporcionó
        if 'amount' in data:
            # Actualizar en la estructura normalizada
            classified_value.value = f"${data['amount']}"
            
            # Actualizar el mensaje para indicar que fue editado
            if 'editado' not in message.content.lower():
                message.content = f"[EDITADO] {message.content}"
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transacción actualizada correctamente',
            'transaction': {
                'id': classified_value.id,
                'message_id': message.id,
                'description': message.content,
                'edited': True
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar la transacción: {str(e)}'}), 500

@financial_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Eliminar una transacción"""
    try:
        # Buscar la transacción en la estructura normalizada
        classified_value = ClassifiedValue.query.get(transaction_id)
        
        if not classified_value:
            return jsonify({'error': 'Transacción no encontrada'}), 404
        
        # Obtener el mensaje asociado
        message = Message.query.get(classified_value.message_id)
        
        # Eliminar primero el valor clasificado
        db.session.delete(classified_value)
        
        # Si se encontró el mensaje, eliminarlo también
        if message:
            db.session.delete(message)
        
        # Confirmar cambios
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transacción eliminada correctamente'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar la transacción: {str(e)}'}), 500