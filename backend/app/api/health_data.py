# backend/app/api/health_data.py
from flask import Blueprint, jsonify, request
from ..models.classified_data import ClassifiedData
from ..models.patient import Patient
from ..models.message import Message
from ..models.category import Category
from ..models.subcategory import Subcategory
from ..models.classified_value import ClassifiedValue
from sqlalchemy import cast, Date, desc, func
import json
from datetime import datetime, timedelta

# Crear blueprint para datos de salud
health_bp = Blueprint('health', __name__, url_prefix='/api/health')

@health_bp.route('/summary', methods=['GET'])
def get_health_summary():
    """Obtener resumen de salud basado en un período"""
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
    else:  # month
        start_date = today - timedelta(days=30)
    
    # Inicializar valores por defecto
    default_response = {
        'physicalVars': {
            'bloodPressure': {'value': '120/80', 'status': 'Normal'},
            'temperature': {'value': '36.5', 'status': 'Normal'},
            'oxygenSaturation': {'value': '98', 'status': 'Normal'},
            'weight': {'value': '70', 'status': 'Normal', 'bmi': '24'}
        },
        'sleep': {'hours': '8', 'status': 'Normal'},
        'cognitiveState': {
            'rating': 8,
            'description': 'Estado cognitivo estable'
        },
        'physicalState': {
            'rating': 8,
            'description': 'Buena movilidad general'
        },
        'emotionalState': {
            'rating': 7,
            'description': 'Estado emocional estable'
        },
        'generalConclusion': 'Bueno'
    }
    
    # Obtener datos clasificados usando la nueva estructura normalizada
    # Primero, obtener los mensajes más recientes
    messages = Message.query.filter(
        Message.patient_id == patient_id,
        Message.created_at >= start_date
    ).order_by(Message.created_at.desc()).limit(10).all()
    
    if not messages:
        return jsonify(default_response)
    
    message_ids = [m.id for m in messages]
    
    # Inicializar variables
    physical_vars = default_response['physicalVars']
    sleep_data = default_response['sleep']
    cognitive_state = default_response['cognitiveState']
    physical_state = default_response['physicalState']
    emotional_state = default_response['emotionalState']
    
    # Obtener valores físicos (temperatura, presión, etc.)
    # Categoría: Salud Física
    physical_category = Category.query.filter(Category.name == 'Salud Física').first()
    if physical_category:
        # Subcategoría: Síntomas (para temperatura, presión, etc.)
        symptoms_subcat = Subcategory.query.filter(
            Subcategory.category_id == physical_category.id,
            Subcategory.name == 'Síntomas'
        ).first()
        
        if symptoms_subcat:
            # Buscar valores relacionados con síntomas
            symptom_values = ClassifiedValue.query.join(
                Message, ClassifiedValue.message_id == Message.id
            ).filter(
                ClassifiedValue.subcategory_id == symptoms_subcat.id,
                Message.id.in_(message_ids)
            ).order_by(Message.created_at.desc()).all()
            
            for value in symptom_values:
                value_text = value.value.lower()
                
                # Temperatura
                if 'temperatura' in value_text:
                    import re
                    temp_match = re.search(r'(\d+(?:[.,]\d+)?)', value_text)
                    if temp_match:
                        temp_value = temp_match.group(1).replace(',', '.')
                        physical_vars['temperature'] = {
                            'value': temp_value,
                            'status': get_status_from_confidence(value.confidence)
                        }
                
                # Presión arterial
                elif 'presión' in value_text or 'presion' in value_text:
                    import re
                    bp_match = re.search(r'(\d+/\d+)', value_text)
                    if bp_match:
                        bp_value = bp_match.group(1)
                        physical_vars['bloodPressure'] = {
                            'value': bp_value,
                            'status': get_status_from_confidence(value.confidence)
                        }
                
                # Oxigenación
                elif 'oxígeno' in value_text or 'oxigeno' in value_text:
                    import re
                    ox_match = re.search(r'(\d+)(?:%|\s*por\s*ciento)?', value_text)
                    if ox_match:
                        ox_value = ox_match.group(1)
                        physical_vars['oxygenSaturation'] = {
                            'value': ox_value,
                            'status': get_status_from_confidence(value.confidence)
                        }
        
        # Subcategoría: Movilidad (para estado físico)
        mobility_subcat = Subcategory.query.filter(
            Subcategory.category_id == physical_category.id,
            Subcategory.name == 'Movilidad'
        ).first()
        
        if mobility_subcat:
            # Buscar valores relacionados con movilidad
            mobility_value = ClassifiedValue.query.join(
                Message, ClassifiedValue.message_id == Message.id
            ).filter(
                ClassifiedValue.subcategory_id == mobility_subcat.id,
                Message.id.in_(message_ids)
            ).order_by(Message.created_at.desc()).first()
            
            if mobility_value:
                physical_state = {
                    'rating': int(mobility_value.confidence * 10),
                    'description': mobility_value.value
                }
        
        # Subcategoría: Sueño
        sleep_subcat = Subcategory.query.filter(
            Subcategory.category_id == physical_category.id,
            Subcategory.name == 'Sueño'
        ).first()
        
        if sleep_subcat:
            # Buscar valores relacionados con sueño
            sleep_value = ClassifiedValue.query.join(
                Message, ClassifiedValue.message_id == Message.id
            ).filter(
                ClassifiedValue.subcategory_id == sleep_subcat.id,
                Message.id.in_(message_ids)
            ).order_by(Message.created_at.desc()).first()
            
            if sleep_value:
                # Extraer horas de sueño
                import re
                hours_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:horas|hs)', sleep_value.value.lower())
                hours = '8'  # Valor por defecto
                
                if hours_match:
                    hours = hours_match.group(1)
                    sleep_hours = float(hours.replace(',', '.'))
                    
                    sleep_data = {
                        'hours': hours,
                        'status': get_status_from_value(sleep_hours)
                    }
    
    # Obtener estado cognitivo
    cognitive_category = Category.query.filter(Category.name == 'Salud Cognitiva').first()
    if cognitive_category:
        # Obtener cualquier subcategoría cognitiva
        cognitive_value = ClassifiedValue.query.join(
            Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
        ).join(
            Message, ClassifiedValue.message_id == Message.id
        ).filter(
            Subcategory.category_id == cognitive_category.id,
            Message.id.in_(message_ids)
        ).order_by(Message.created_at.desc()).first()
        
        if cognitive_value:
            cognitive_state = {
                'rating': int(cognitive_value.confidence * 10),
                'description': cognitive_value.value
            }
    
    # Obtener estado emocional
    emotional_category = Category.query.filter(Category.name == 'Estado Emocional').first()
    if emotional_category:
        # Obtener cualquier subcategoría emocional
        emotional_value = ClassifiedValue.query.join(
            Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
        ).join(
            Message, ClassifiedValue.message_id == Message.id
        ).filter(
            Subcategory.category_id == emotional_category.id,
            Message.id.in_(message_ids)
        ).order_by(Message.created_at.desc()).first()
        
        if emotional_value:
            emotional_state = {
                'rating': int(emotional_value.confidence * 10),
                'description': emotional_value.value
            }
    
    # Calcular conclusión general
    ratings = [
        cognitive_state['rating'],
        physical_state['rating'],
        emotional_state['rating']
    ]
    avg_rating = sum(ratings) / len(ratings)
    
    if avg_rating >= 7:
        conclusion = 'Bueno'
    elif avg_rating >= 5:
        conclusion = 'Regular'
    else:
        conclusion = 'Malo'
    
    # Resultado
    result = {
        'physicalVars': physical_vars,
        'sleep': sleep_data,
        'cognitiveState': cognitive_state,
        'physicalState': physical_state,
        'emotionalState': emotional_state,
        'generalConclusion': conclusion
    }
    
    return jsonify(result)

@health_bp.route('/metrics/<metric_type>', methods=['GET'])
def get_metrics_history(metric_type):
    """Obtener historial de métricas específicas"""
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
    else:  # month
        start_date = today - timedelta(days=30)
    
    # Extraer métricas según el tipo
    metrics = []
    
    # Determinar qué subcategoría buscar según el tipo de métrica
    subcategory_id = None
    physical_category = Category.query.filter(Category.name == 'Salud Física').first()
    
    if physical_category:
        if metric_type == 'blood_pressure':
            # Buscar la subcategoría de síntomas
            symptoms_subcat = Subcategory.query.filter(
                Subcategory.category_id == physical_category.id,
                Subcategory.name == 'Síntomas'
            ).first()
            
            if symptoms_subcat:
                subcategory_id = symptoms_subcat.id
        
        elif metric_type == 'temperature':
            # Buscar la subcategoría de síntomas
            symptoms_subcat = Subcategory.query.filter(
                Subcategory.category_id == physical_category.id,
                Subcategory.name == 'Síntomas'
            ).first()
            
            if symptoms_subcat:
                subcategory_id = symptoms_subcat.id
    
    if subcategory_id:
        # Obtener valores clasificados para la subcategoría
        values = ClassifiedValue.query.join(
            Message, ClassifiedValue.message_id == Message.id
        ).filter(
            ClassifiedValue.subcategory_id == subcategory_id,
            Message.patient_id == patient_id,
            Message.created_at >= start_date
        ).order_by(Message.created_at).all()
        
        for value in values:
            date_str = value.created_at.strftime('%Y-%m-%d')
            
            if metric_type == 'blood_pressure' and 'presión' in value.value.lower():
                import re
                bp_match = re.search(r'(\d+/\d+)', value.value)
                if bp_match:
                    metrics.append({
                        'date': date_str,
                        'value': bp_match.group(1),
                        'status': get_status_from_confidence(value.confidence)
                    })
            
            elif metric_type == 'temperature' and 'temperatura' in value.value.lower():
                import re
                temp_match = re.search(r'(\d+(?:[.,]\d+)?)', value.value)
                if temp_match:
                    metrics.append({
                        'date': date_str,
                        'value': temp_match.group(1).replace(',', '.'),
                        'status': get_status_from_confidence(value.confidence)
                    })
    
    return jsonify(metrics)

@health_bp.route('/history', methods=['GET'])
def get_health_history():
    """
    Obtiene el historial de variables de salud con filtros opcionales
    
    Query params:
    - patient_id: ID del paciente (obligatorio)
    - period: 'day', 'week', 'month' (opcional, default: 'day')
    - category: 'physical', 'cognitive', 'emotional', 'medication' (opcional)
    """
    # Obtener parámetros de query
    patient_id = request.args.get('patient_id', type=int)
    period = request.args.get('period', 'day')
    category_filter = request.args.get('category', None)
    
    # Validar paciente
    if not patient_id:
        return jsonify({'error': 'Se requiere ID de paciente'}), 400
    
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
    # Calcular fecha de inicio según período
    today = datetime.now().date()
    if period == 'day':
        start_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today - timedelta(days=30)
    else:
        return jsonify({"error": "Período no válido. Use 'day', 'week' o 'month'"}), 400
    
    # Construir query base usando la nueva estructura normalizada
    query = ClassifiedValue.query.join(
        Message, ClassifiedValue.message_id == Message.id
    ).join(
        Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
    ).join(
        Category, Subcategory.category_id == Category.id
    ).filter(
        Message.patient_id == patient_id,
        cast(Message.created_at, Date) >= start_date
    )
    
    # Aplicar filtro de categoría si se especifica
    if category_filter:
        category_map = {
            'physical': 'Salud Física',
            'cognitive': 'Salud Cognitiva',
            'emotional': 'Estado Emocional',
            'medication': 'Medicación'
        }
        
        category_name = category_map.get(category_filter)
        if category_name:
            query = query.filter(Category.name == category_name)
    
    # Ordenar por fecha más reciente
    query = query.order_by(Message.created_at.desc())
    
    # Ejecutar consulta
    results = query.all()
    
    # Formatear resultados
    history_items = []
    
    for value in results:
        # Obtener detalles del mensaje, categoría y subcategoría
        message = value.message
        subcategory = value.subcategory
        category = subcategory.category
        
        # Crear item para el historial
        history_item = {
            "id": value.id,
            "date": value.created_at.strftime("%d/%m/%Y"),
            "time": value.created_at.strftime("%H:%M"),
            "original_text": message.content[:100] + "..." if len(message.content) > 100 else message.content,
            "category": category.name,
            "subcategory": subcategory.name,
            "value": value.value,
            "rating": int(value.confidence * 10),
            "confidence": value.confidence
        }
        
        history_items.append(history_item)
    
    return jsonify({"history": history_items})

def get_status_from_confidence(confidence):
    """Convertir valor de confianza a estado"""
    if confidence >= 0.8:
        return 'Normal'
    elif confidence >= 0.5:
        return 'Moderado'
    else:
        return 'Bajo'

def get_status_from_value(value):
    """Determinar estado basado en valor (específico para horas de sueño)"""
    if value >= 7:
        return 'Normal'
    elif value >= 5:
        return 'Moderado'
    else:
        return 'Bajo'