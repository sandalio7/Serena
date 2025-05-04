# backend/app/api/health_data.py
from flask import Blueprint, jsonify, request
from ..models.classified_data import ClassifiedData
from ..models.patient import Patient
from ..models.message import Message
from sqlalchemy import cast, Date
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
    
    # Obtener datos clasificados para el período
    data_query = ClassifiedData.query.filter(
        ClassifiedData.patient_id == patient_id,
        ClassifiedData.created_at >= start_date
    ).order_by(ClassifiedData.created_at.desc()).all()
    
    # Si no hay datos, devolver un conjunto predeterminado
    if not data_query:
        return jsonify({
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
        })
    
    # Extraer el último registro para datos más recientes
    latest_data = data_query[0]
    
    # Procesar datos físicos
    physical_vars = {
        'bloodPressure': {'value': '130/85', 'status': 'Normal'},
        'temperature': {'value': '36,8', 'status': 'Normal'},
        'oxygenSaturation': {'value': '95', 'status': 'Moderado'},
        'weight': {'value': '71', 'status': 'Moderado', 'bmi': '27'}
    }
    
    if latest_data.physical_health:
        physical_data = json.loads(latest_data.physical_health)
        
        # Buscar subcategorías específicas
        for subcategory in physical_data:
            subcat_name = subcategory.get('nombre', '').lower()
            
            if 'presión' in subcat_name:
                physical_vars['bloodPressure'] = {
                    'value': subcategory.get('valor', '120/80'),
                    'status': get_status_from_confidence(subcategory.get('confianza', 0.7))
                }
            elif 'temperatura' in subcat_name:
                physical_vars['temperature'] = {
                    'value': subcategory.get('valor', '36.5'),
                    'status': get_status_from_confidence(subcategory.get('confianza', 0.7))
                }
            elif 'oxígeno' in subcat_name or 'oxigeno' in subcat_name:
                physical_vars['oxygenSaturation'] = {
                    'value': subcategory.get('valor', '98'),
                    'status': get_status_from_confidence(subcategory.get('confianza', 0.7))
                }
            elif 'peso' in subcat_name:
                # Extraer valor de IMC si está en el texto
                valor = subcategory.get('valor', '70')
                bmi = '24'  # Valor por defecto
                if 'imc' in valor.lower():
                    import re
                    bmi_match = re.search(r'imc\s*[:-]?\s*(\d+)', valor.lower())
                    if bmi_match:
                        bmi = bmi_match.group(1)
                
                physical_vars['weight'] = {
                    'value': valor.split(' ')[0] if ' ' in valor else valor,
                    'status': get_status_from_confidence(subcategory.get('confianza', 0.7)),
                    'bmi': bmi
                }
    
    # Procesar datos de sueño
    sleep_data = {
        'hours': '5,5',
        'status': 'Bajo'
    }
    
    if latest_data.physical_health:
        physical_data = json.loads(latest_data.physical_health)
        
        for subcategory in physical_data:
            subcat_name = subcategory.get('nombre', '').lower()
            
            if 'sueño' in subcat_name or 'sueno' in subcat_name or 'dormir' in subcat_name:
                # Extraer horas de sueño
                valor = subcategory.get('valor', '')
                hours = '8'  # Valor por defecto
                import re
                hours_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:horas|hs)', valor.lower())
                if hours_match:
                    hours = hours_match.group(1)
                
                sleep_data = {
                    'hours': hours,
                    'status': get_status_from_value(float(hours.replace(',', '.')))
                }
    
    # Procesar estado cognitivo
    cognitive_state = {
        'rating': 4,
        'description': 'Se lo notó desorientado durante toda la tarde'
    }
    
    if latest_data.cognitive_health:
        cognitive_data = json.loads(latest_data.cognitive_health)
        
        # Si hay datos, usar el primero como descripción general
        if cognitive_data and len(cognitive_data) > 0:
            first_item = cognitive_data[0]
            confidence = first_item.get('confianza', 0.5)
            rating = int(confidence * 10)  # Convertir confianza a escala de 1-10
            
            cognitive_state = {
                'rating': rating,
                'description': first_item.get('valor', 'Sin información')
            }
    
    # Procesar estado físico
    physical_state = {
        'rating': 7,
        'description': 'Caminó solo dentro de la casa sin asistencia'
    }
    
    if latest_data.physical_health:
        physical_data = json.loads(latest_data.physical_health)
        
        # Buscar subcategoría de movilidad
        for subcategory in physical_data:
            subcat_name = subcategory.get('nombre', '').lower()
            
            if 'movilidad' in subcat_name:
                confidence = subcategory.get('confianza', 0.7)
                rating = int(confidence * 10)  # Convertir confianza a escala de 1-10
                
                physical_state = {
                    'rating': rating,
                    'description': subcategory.get('valor', 'Sin información')
                }
    
    # Procesar estado emocional
    emotional_state = {
        'rating': 6,
        'description': 'Participó con desgano en actividades'
    }
    
    if latest_data.emotional_state:
        emotional_data = json.loads(latest_data.emotional_state)
        
        # Si hay datos, usar el primero como descripción general
        if emotional_data and len(emotional_data) > 0:
            first_item = emotional_data[0]
            confidence = first_item.get('confianza', 0.6)
            rating = int(confidence * 10)  # Convertir confianza a escala de 1-10
            
            emotional_state = {
                'rating': rating,
                'description': first_item.get('valor', 'Sin información')
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
    
    # Obtener datos clasificados para el período
    data_query = ClassifiedData.query.filter(
        ClassifiedData.patient_id == patient_id,
        ClassifiedData.created_at >= start_date
    ).order_by(ClassifiedData.created_at).all()
    
    # Extraer métricas según el tipo
    metrics = []
    
    for data in data_query:
        date_str = data.created_at.strftime('%Y-%m-%d')
        
        if metric_type == 'blood_pressure' and data.physical_health:
            physical_data = json.loads(data.physical_health)
            
            for subcategory in physical_data:
                subcat_name = subcategory.get('nombre', '').lower()
                if 'presión' in subcat_name:
                    metrics.append({
                        'date': date_str,
                        'value': subcategory.get('valor', '120/80'),
                        'status': get_status_from_confidence(subcategory.get('confianza', 0.7))
                    })
                    break  # Solo una métrica por fecha
                    
        elif metric_type == 'temperature' and data.physical_health:
            physical_data = json.loads(data.physical_health)
            
            for subcategory in physical_data:
                subcat_name = subcategory.get('nombre', '').lower()
                if 'temperatura' in subcat_name:
                    metrics.append({
                        'date': date_str,
                        'value': subcategory.get('valor', '36.5'),
                        'status': get_status_from_confidence(subcategory.get('confianza', 0.7))
                    })
                    break  # Solo una métrica por fecha
    
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
    category = request.args.get('category', None)
    
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
    
    # Construir query base - usamos created_at en lugar de timestamp
    query = ClassifiedData.query.filter(
        ClassifiedData.patient_id == patient_id,
        cast(ClassifiedData.created_at, Date) >= start_date
    ).order_by(
        ClassifiedData.created_at.desc()
    )
    
    # Aplicar filtro de categoría si se especifica
    if category:
        if category == 'physical':
            query = query.filter(ClassifiedData.physical_health.isnot(None))
        elif category == 'cognitive':
            query = query.filter(ClassifiedData.cognitive_health.isnot(None))
        elif category == 'emotional':
            query = query.filter(ClassifiedData.emotional_state.isnot(None))
        elif category == 'medication':
            query = query.filter(ClassifiedData.medication.isnot(None))
    
    # Ejecutar consulta
    results = query.all()
    
    # Formatear resultados
    history_items = []
    for item in results:
        # Buscar el mensaje original
        message = Message.query.get(item.message_id)
        
        # Crear item básico con información común
        history_item = {
            "id": item.id,
            "date": item.created_at.strftime("%d/%m/%Y"),
            "time": item.created_at.strftime("%H:%M"),
            "original_text": message.content[:100] + "..." if len(message.content) > 100 else message.content,
        }
        
        # Añadir información específica según las categorías disponibles
        if item.physical_health:
            try:
                physical_data = json.loads(item.physical_health)
                # Verificar si physical_data es una lista o un diccionario
                if isinstance(physical_data, list):
                    for subcat in physical_data:
                        if isinstance(subcat, dict):
                            history_items.append({
                                **history_item,
                                "category": "Salud Física",
                                "subcategory": subcat.get('nombre', ''),
                                "value": subcat.get('valor', ''),
                                "rating": int(subcat.get('confianza', 0.7) * 10),
                                "confidence": subcat.get('confianza', 0.7)
                            })
                        elif isinstance(subcat, str):
                            # Si es un string, usar como valor directamente
                            history_items.append({
                                **history_item,
                                "category": "Salud Física",
                                "subcategory": "General",
                                "value": subcat,
                                "rating": 7,  # Valor por defecto
                                "confidence": 0.7
                            })
                elif isinstance(physical_data, dict):
                    history_items.append({
                        **history_item,
                        "category": "Salud Física",
                        "subcategory": physical_data.get('nombre', 'General'),
                        "value": physical_data.get('valor', ''),
                        "rating": int(physical_data.get('confianza', 0.7) * 10),
                        "confidence": physical_data.get('confianza', 0.7)
                    })
            except (json.JSONDecodeError, AttributeError) as e:
                # Si hay error al decodificar, usar el texto crudo
                history_items.append({
                    **history_item,
                    "category": "Salud Física",
                    "subcategory": "General",
                    "value": str(item.physical_health),
                    "rating": 7,  # Valor por defecto
                    "confidence": 0.7
                })
        
        if item.cognitive_health:
            try:
                cognitive_data = json.loads(item.cognitive_health)
                # Mismo patrón que arriba
                if isinstance(cognitive_data, list):
                    for subcat in cognitive_data:
                        if isinstance(subcat, dict):
                            history_items.append({
                                **history_item,
                                "category": "Estado Cognitivo",
                                "subcategory": subcat.get('nombre', ''),
                                "value": subcat.get('valor', ''),
                                "rating": int(subcat.get('confianza', 0.7) * 10),
                                "confidence": subcat.get('confianza', 0.7)
                            })
                        elif isinstance(subcat, str):
                            history_items.append({
                                **history_item,
                                "category": "Estado Cognitivo",
                                "subcategory": "General",
                                "value": subcat,
                                "rating": 7,
                                "confidence": 0.7
                            })
                elif isinstance(cognitive_data, dict):
                    history_items.append({
                        **history_item,
                        "category": "Estado Cognitivo",
                        "subcategory": cognitive_data.get('nombre', 'General'),
                        "value": cognitive_data.get('valor', ''),
                        "rating": int(cognitive_data.get('confianza', 0.7) * 10),
                        "confidence": cognitive_data.get('confianza', 0.7)
                    })
            except (json.JSONDecodeError, AttributeError) as e:
                history_items.append({
                    **history_item,
                    "category": "Estado Cognitivo",
                    "subcategory": "General",
                    "value": str(item.cognitive_health),
                    "rating": 7,
                    "confidence": 0.7
                })
        
        if item.emotional_state:
            try:
                emotional_data = json.loads(item.emotional_state)
                # Mismo patrón
                if isinstance(emotional_data, list):
                    for subcat in emotional_data:
                        if isinstance(subcat, dict):
                            history_items.append({
                                **history_item,
                                "category": "Estado Emocional",
                                "subcategory": subcat.get('nombre', ''),
                                "value": subcat.get('valor', ''),
                                "rating": int(subcat.get('confianza', 0.7) * 10),
                                "confidence": subcat.get('confianza', 0.7)
                            })
                        elif isinstance(subcat, str):
                            history_items.append({
                                **history_item,
                                "category": "Estado Emocional",
                                "subcategory": "General",
                                "value": subcat,
                                "rating": 7,
                                "confidence": 0.7
                            })
                elif isinstance(emotional_data, dict):
                    history_items.append({
                        **history_item,
                        "category": "Estado Emocional",
                        "subcategory": emotional_data.get('nombre', 'General'),
                        "value": emotional_data.get('valor', ''),
                        "rating": int(emotional_data.get('confianza', 0.7) * 10),
                        "confidence": emotional_data.get('confianza', 0.7)
                    })
            except (json.JSONDecodeError, AttributeError) as e:
                history_items.append({
                    **history_item,
                    "category": "Estado Emocional",
                    "subcategory": "General",
                    "value": str(item.emotional_state),
                    "rating": 7,
                    "confidence": 0.7
                })
        
        if item.medication:
            try:
                medication_data = json.loads(item.medication)
                # Mismo patrón
                if isinstance(medication_data, list):
                    for subcat in medication_data:
                        if isinstance(subcat, dict):
                            history_items.append({
                                **history_item,
                                "category": "Medicación",
                                "subcategory": subcat.get('nombre', ''),
                                "value": subcat.get('valor', ''),
                                "rating": int(subcat.get('confianza', 0.7) * 10),
                                "confidence": subcat.get('confianza', 0.7)
                            })
                        elif isinstance(subcat, str):
                            history_items.append({
                                **history_item,
                                "category": "Medicación",
                                "subcategory": "General",
                                "value": subcat,
                                "rating": 7,
                                "confidence": 0.7
                            })
                elif isinstance(medication_data, dict):
                    history_items.append({
                        **history_item,
                        "category": "Medicación",
                        "subcategory": medication_data.get('nombre', 'General'),
                        "value": medication_data.get('valor', ''),
                        "rating": int(medication_data.get('confianza', 0.7) * 10),
                        "confidence": medication_data.get('confianza', 0.7)
                    })
            except (json.JSONDecodeError, AttributeError) as e:
                history_items.append({
                    **history_item,
                    "category": "Medicación",
                    "subcategory": "General",
                    "value": str(item.medication),
                    "rating": 7,
                    "confidence": 0.7
                })
    
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