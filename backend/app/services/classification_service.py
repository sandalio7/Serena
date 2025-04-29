# backend/app/services/classification_service.py
import json
from ..extensions import db
from ..models.message import Message
from ..models.classified_data import ClassifiedData
from ..models.caregiver import Caregiver
from .gemini_service import classify_message, extract_data_by_category

def process_whatsapp_message(message_content, whatsapp_message_id, phone_number):
    """
    Procesa un mensaje de WhatsApp: clasifica el contenido y guarda los resultados
    
    Args:
        message_content (str): Contenido del mensaje
        whatsapp_message_id (str): ID del mensaje en WhatsApp
        phone_number (str): Número de teléfono del remitente
        
    Returns:
        tuple: (estado, mensaje, datos_clasificados)
    """
    try:
        # 1. Buscar el cuidador por número de teléfono
        caregiver = Caregiver.get_by_phone(phone_number)
        if not caregiver:
            return False, f"No se encontró un cuidador registrado con el número {phone_number}", None
        
        # 2. Verificar si ya existe un mensaje con este ID
        existing_message = Message.query.filter_by(whatsapp_message_id=whatsapp_message_id).first()
        if existing_message:
            return False, "Este mensaje ya ha sido procesado anteriormente", None
        
        # 3. Crear nuevo mensaje
        message = Message(
            content=message_content,
            whatsapp_message_id=whatsapp_message_id,
            caregiver_id=caregiver.id,
            patient_id=caregiver.patient_id
        )
        db.session.add(message)
        db.session.flush()  # Para obtener el ID sin hacer commit
        
        # 4. Clasificar el mensaje con Gemini AI
        classified_data_raw = classify_message(message_content)
        
        # 5. Extraer datos por categoría
        physical_health = extract_data_by_category(classified_data_raw, "Salud Física")
        cognitive_health = extract_data_by_category(classified_data_raw, "Salud Cognitiva")
        emotional_state = extract_data_by_category(classified_data_raw, "Estado Emocional")
        medication = extract_data_by_category(classified_data_raw, "Medicación")
        expenses = extract_data_by_category(classified_data_raw, "Gastos")
        
        # 6. Crear registro de datos clasificados
        classified_data = ClassifiedData(
            raw_data=json.dumps(classified_data_raw),
            physical_health=json.dumps(physical_health) if physical_health['detectada'] else None,
            cognitive_health=json.dumps(cognitive_health) if cognitive_health['detectada'] else None,
            emotional_state=json.dumps(emotional_state) if emotional_state['detectada'] else None,
            medication=json.dumps(medication) if medication['detectada'] else None,
            expenses=json.dumps(expenses) if expenses['detectada'] else None,
            summary=classified_data_raw.get('resumen', ''),
            message_id=message.id,
            patient_id=caregiver.patient_id
        )
        db.session.add(classified_data)
        
        # 7. Guardar cambios en la base de datos
        db.session.commit()
        
        return True, "Mensaje procesado y clasificado correctamente", classified_data
        
    except Exception as e:
        db.session.rollback()
        print(f"Error procesando mensaje: {str(e)}")
        return False, f"Error procesando mensaje: {str(e)}", None