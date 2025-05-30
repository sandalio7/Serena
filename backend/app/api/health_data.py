# backend/app/api/health_data.py
from flask import Blueprint, jsonify, request
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
    
    # Calcular fecha de hace 7 días para determinar mediciones recientes
    week_ago = today - timedelta(days=7)
    
    # Inicializar valores vitales con información sobre disponibilidad
    physical_vars = {
        'bloodPressure': {
            'available': False,
            'value': None,
            'status': None,
            'lastMeasured': None
        },
        'temperature': {
            'available': False,
            'value': None,
            'status': None,
            'lastMeasured': None
        },
        'oxygenSaturation': {
            'available': False,
            'value': None,
            'status': None,
            'lastMeasured': None
        },
        'weight': {
            'available': False,
            'value': None,
            'status': None,
            'lastMeasured': None
        }
    }
    
    # Valores normales de referencia (siempre disponibles)
    normal_values = {
        'bloodPressure': { 'systolic': 130, 'diastolic': 80 },
        'temperature': 36.5,
        'oxygenation': 98
    }
    
    # Inicializar otros datos con valores predeterminados
    sleep_data = {
        'hours': '8', 
        'status': 'Normal'
    }
    
    cognitive_state = {
        'rating': 8,
        'description': 'Estado cognitivo estable'
    }
    
    physical_state = {
        'rating': 8,
        'description': 'Buena movilidad general'
    }
    
    emotional_state = {
        'rating': 7,
        'description': 'Estado emocional estable'
    }
    
    # Debug: Registrar información de búsqueda
    print(f"Buscando datos de salud para paciente {patient_id} desde {start_date}")
    
    # Verificar si hay mensajes para este paciente en el período
    messages = Message.query.filter(
        Message.patient_id == patient_id,
        Message.created_at >= start_date
    ).order_by(Message.created_at.desc()).all()
    
    print(f"Encontrados {len(messages)} mensajes para el paciente {patient_id}")
    
    if not messages:
        print("No se encontraron mensajes, devolviendo respuesta con valores no disponibles")
        return jsonify({
            'physicalVars': physical_vars,
            'normalValues': normal_values,
            'sleep': sleep_data,
            'cognitiveState': cognitive_state,
            'physicalState': physical_state,
            'emotionalState': emotional_state,
            'generalConclusion': 'Regular'
        })
    
    message_ids = [m.id for m in messages]
    
    # Contar clasificaciones por categoría (para debug)
    health_values_count = 0
    
    # Obtener valores físicos (temperatura, presión, etc.)
    # Categoría: Salud Física
    physical_category = Category.query.filter(Category.name == 'Salud Física').first()
    if physical_category:
        print(f"Encontrada categoría: {physical_category.name} (ID: {physical_category.id})")
        
        # Obtener todas las subcategorías físicas
        subcategories = Subcategory.query.filter(Subcategory.category_id == physical_category.id).all()
        print(f"Subcategorías físicas encontradas: {[s.name for s in subcategories]}")
        
        # Subcategoría: Síntomas (para temperatura, presión, etc.)
        symptoms_subcat = next((s for s in subcategories if s.name == 'Síntomas'), None)
        
        if symptoms_subcat:
            print(f"Encontrada subcategoría: {symptoms_subcat.name} (ID: {symptoms_subcat.id})")
            
            # Buscar valores relacionados con síntomas
            symptom_values = ClassifiedValue.query.join(
                Message, ClassifiedValue.message_id == Message.id
            ).filter(
                ClassifiedValue.subcategory_id == symptoms_subcat.id,
                Message.id.in_(message_ids)
            ).order_by(Message.created_at.desc()).all()
            
            print(f"Valores de síntomas encontrados: {len(symptom_values)}")
            health_values_count += len(symptom_values)
            
            for value in symptom_values:
                message = Message.query.get(value.message_id)
                print(f"Procesando valor: {value.value} (confianza: {value.confidence})")
                value_text = value.value.lower()
                
                # Temperatura
                if 'temperatura' in value_text and not physical_vars['temperature']['available']:
                    import re
                    temp_match = re.search(r'(\d+(?:[.,]\d+)?)', value_text)
                    if temp_match:
                        temp_value = temp_match.group(1).replace(',', '.')
                        physical_vars['temperature'] = {
                            'available': True,
                            'value': temp_value,
                            'status': get_status_from_confidence(value.confidence),
                            'lastMeasured': message.created_at.isoformat(),
                            'recent': message.created_at >= week_ago
                        }
                        print(f"Actualizada temperatura: {temp_value}, fecha: {message.created_at}")
                
                # Presión arterial
                elif ('presión' in value_text or 'presion' in value_text) and not physical_vars['bloodPressure']['available']:
                    import re
                    bp_match = re.search(r'(\d+/\d+)', value_text)
                    if bp_match:
                        bp_value = bp_match.group(1)
                        physical_vars['bloodPressure'] = {
                            'available': True,
                            'value': bp_value,
                            'status': get_status_from_confidence(value.confidence),
                            'lastMeasured': message.created_at.isoformat(),
                            'recent': message.created_at >= week_ago
                        }
                        print(f"Actualizada presión arterial: {bp_value}, fecha: {message.created_at}")
                
                # Oxigenación
                elif ('oxígeno' in value_text or 'oxigeno' in value_text) and not physical_vars['oxygenSaturation']['available']:
                    import re
                    ox_match = re.search(r'(\d+)(?:%|\s*por\s*ciento)?', value_text)
                    if ox_match:
                        ox_value = ox_match.group(1)
                        physical_vars['oxygenSaturation'] = {
                            'available': True,
                            'value': ox_value,
                            'status': get_status_from_confidence(value.confidence),
                            'lastMeasured': message.created_at.isoformat(),
                            'recent': message.created_at >= week_ago
                        }
                        print(f"Actualizada oxigenación: {ox_value}, fecha: {message.created_at}")
        
        # Subcategoría: Movilidad (para estado físico)
        mobility_subcat = next((s for s in subcategories if s.name == 'Movilidad'), None)
        
        if mobility_subcat:
            print(f"Encontrada subcategoría: {mobility_subcat.name} (ID: {mobility_subcat.id})")
            
            # Buscar valores relacionados con movilidad
            mobility_value = ClassifiedValue.query.join(
                Message, ClassifiedValue.message_id == Message.id
            ).filter(
                ClassifiedValue.subcategory_id == mobility_subcat.id,
                Message.id.in_(message_ids)
            ).order_by(Message.created_at.desc()).first()
            
            if mobility_value:
                health_values_count += 1
                print(f"Encontrado valor de movilidad: {mobility_value.value}")
                physical_state = {
                    'rating': int(mobility_value.confidence * 10),
                    'description': mobility_value.value
                }
                print(f"Actualizado estado físico: {physical_state}")
        
        # Subcategoría: Sueño
        sleep_subcat = next((s for s in subcategories if s.name == 'Sueño'), None)
        
        if sleep_subcat:
            print(f"Encontrada subcategoría: {sleep_subcat.name} (ID: {sleep_subcat.id})")
            
            # Buscar valores relacionados con sueño
            sleep_value = ClassifiedValue.query.join(
                Message, ClassifiedValue.message_id == Message.id
            ).filter(
                ClassifiedValue.subcategory_id == sleep_subcat.id,
                Message.id.in_(message_ids)
            ).order_by(Message.created_at.desc()).first()
            
            if sleep_value:
                health_values_count += 1
                print(f"Encontrado valor de sueño: {sleep_value.value}")
                
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
                    print(f"Actualizado sueño: {sleep_data}")
    else:
        print("No se encontró la categoría 'Salud Física'")
    
    # Obtener estado cognitivo
    cognitive_category = Category.query.filter(Category.name == 'Salud Cognitiva').first()
    if cognitive_category:
        print(f"Encontrada categoría: {cognitive_category.name} (ID: {cognitive_category.id})")
        
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
            health_values_count += 1
            print(f"Encontrado valor cognitivo: {cognitive_value.value}")
            cognitive_state = {
                'rating': int(cognitive_value.confidence * 10),
                'description': cognitive_value.value
            }
            print(f"Actualizado estado cognitivo: {cognitive_state}")
    else:
        print("No se encontró la categoría 'Salud Cognitiva'")
    
    # Obtener estado emocional
    emotional_category = Category.query.filter(Category.name == 'Estado Emocional').first()
    if emotional_category:
        print(f"Encontrada categoría: {emotional_category.name} (ID: {emotional_category.id})")
        
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
            health_values_count += 1
            print(f"Encontrado valor emocional: {emotional_value.value}")
            emotional_state = {
                'rating': int(emotional_value.confidence * 10),
                'description': emotional_value.value
            }
            print(f"Actualizado estado emocional: {emotional_state}")
    else:
        print("No se encontró la categoría 'Estado Emocional'")
    
    print(f"Total de valores de salud encontrados: {health_values_count}")
    
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
        'normalValues': normal_values,
        'sleep': sleep_data,
        'cognitiveState': cognitive_state,
        'physicalState': physical_state,
        'emotionalState': emotional_state,
        'generalConclusion': conclusion
    }
    
    print(f"Respuesta final: {result}")
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
    - category: 'physical', 'cognitive', 'emotional', 'medication', 'autonomy' (opcional)
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
    
    # Construir query base usando solo la estructura normalizada
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
    
    # FILTRO CRÍTICO: Excluir explícitamente la categoría "Gastos" del dashboard de salud
    query = query.filter(Category.name != 'Gastos')
    
    # Aplicar filtro de categoría si se especifica
    if category_filter:
        category_map = {
            'physical': 'Salud Física',
            'cognitive': 'Salud Cognitiva',
            'emotional': 'Estado Emocional',
            'medication': 'Medicación',  # NUEVO: Soporte para filtrar por medicación
            'autonomy': 'Autonomía'
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
        
        # Mapear nombre de categoría para el frontend
        category_frontend_map = {
            'Salud Física': 'physical',
            'Salud Cognitiva': 'cognitive',
            'Estado Emocional': 'emotional',
            'Medicación': 'medication',
            'Autonomía': 'autonomy'
        }
        
        frontend_category = category_frontend_map.get(category.name, 'other')
        
        # Crear item para el historial
        history_item = {
            "id": value.id,
            "date": value.created_at.strftime("%d/%m/%Y"),
            "time": value.created_at.strftime("%H:%M"),
            "original_text": message.content[:100] + "..." if len(message.content) > 100 else message.content,
            "category": frontend_category,  # Categoría en formato frontend
            "categoryName": category.name,  # Nombre completo de la categoría para mostrar
            "subcategory": subcategory.name,
            "value": value.value,
            "description": value.value,  # Alias para compatibilidad con frontend
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