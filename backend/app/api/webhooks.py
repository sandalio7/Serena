import os
import logging
from flask import Blueprint, request, jsonify
from app.services.classification_service import ClassificationService
from app.models.caregiver import Caregiver
from app.extensions import db

# Configuración de logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializar Blueprint
webhook_bp = Blueprint('webhooks', __name__)  # Cambiado de webhooks_bp a webhook_bp

# Token de verificación para el webhook
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
if not VERIFY_TOKEN:
    logger.warning("WHATSAPP_VERIFY_TOKEN no configurado en .env. Usando token predeterminado.")
    VERIFY_TOKEN = "serena-secret-key"  # Token predeterminado solo como fallback

# Inicializar servicio de clasificación
classification_service = ClassificationService()

@webhook_bp.route("/api/webhook/test", methods=["GET"])
def test_webhook():
    """Ruta de prueba para verificar que el blueprint está registrado"""
    return jsonify({"status": "success", "message": "Webhook blueprint is working"}), 200

@webhook_bp.route("/api/webhook/whatsapp", methods=["GET", "POST"])  # Cambiado de webhooks_bp a webhook_bp
def whatsapp_webhook():
    """
    Endpoint para recibir y procesar mensajes de WhatsApp.
    Compatible con Twilio, MessageBird o versión directa de WhatsApp Business API.
    """
    if request.method == "GET":
        # Verificación del webhook
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        logger.info(f"Recibida solicitud de verificación: modo={mode}, token={token}")
        
        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                logger.info("Webhook verificado exitosamente!")
                return challenge, 200
            else:
                logger.warning("Verificación fallida - token incorrecto")
                return "Verificación fallida", 403
                
        return "Parámetros incorrectos", 400
    
    elif request.method == "POST":
        # Procesamiento de mensajes entrantes
        try:
            data = request.json
            logger.info(f"Mensaje webhook recibido: {data}")
            
            # Detectar tipo de proveedor (Twilio, MessageBird, WhatsApp directo)
            provider_type = detect_provider(request)
            
            if provider_type == "whatsapp_cloud":
                return process_whatsapp_cloud_message(data)
            elif provider_type == "twilio":
                return process_twilio_message(data)
            elif provider_type == "messagebird":
                return process_messagebird_message(data)
            else:
                # Si no podemos detectar el proveedor, intentar un procesamiento genérico
                return process_generic_message(data)
                
        except Exception as e:
            logger.error(f"Error procesando webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

def detect_provider(request):
    """
    Detecta el proveedor basado en los headers y formato del mensaje
    """
    # Comprobar headers específicos de cada proveedor
    user_agent = request.headers.get("User-Agent", "").lower()
    content_type = request.headers.get("Content-Type", "").lower()
    
    if "twilio" in user_agent:
        return "twilio"
    elif "messagebird" in user_agent:
        return "messagebird"
    
    # Si no se detecta por headers, intentar por el formato del json
    data = request.json
    if not data:
        return "unknown"
    
    # WhatsApp Cloud API format detection
    if "object" in data and data.get("object") == "whatsapp_business_account":
        return "whatsapp_cloud"
    # Twilio format detection
    elif "SmsMessageSid" in data:
        return "twilio"
    # MessageBird format detection
    elif "message" in data and "originator" in data.get("message", {}):
        return "messagebird"
        
    # Default
    return "unknown"

def process_whatsapp_cloud_message(data):
    """
    Procesa mensajes del formato de WhatsApp Cloud API
    """
    try:
        # Estructura de WhatsApp Cloud API
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])
        
        if not messages:
            logger.info("No hay mensajes en la notificación de WhatsApp")
            return jsonify({"status": "success", "message": "No message to process"}), 200
        
        message = messages[0]
        message_id = message.get('id')
        
        # Solo procesar mensajes de texto
        if message.get('type') != 'text':
            logger.info(f"Mensaje recibido no es de texto. Tipo: {message.get('type')}")
            return jsonify({"status": "success", "message": "Non-text message ignored"}), 200
        
        # Obtener texto del mensaje
        text = message.get('text', {}).get('body', '')
        
        # Obtener número de teléfono
        phone_number = message.get('from', '')
        
        # Buscar cuidador y paciente asociado
        patient_id = find_patient_by_caregiver(phone_number)
        
        # Procesar el mensaje
        result = classification_service.process_message(text, phone_number, patient_id)
        
        return jsonify({"status": "success", "result": result}), 200
    
    except Exception as e:
        logger.error(f"Error procesando mensaje de WhatsApp Cloud API: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def process_twilio_message(data):
    """Procesa mensajes del formato de Twilio"""
    try:
        # Estructura de Twilio
        message_id = data.get('SmsMessageSid', '')
        text = data.get('Body', '')
        phone_number = data.get('From', '').replace('whatsapp:', '')
        
        # Buscar cuidador y paciente asociado
        patient_id = find_patient_by_caregiver(phone_number)
        
        # Procesar el mensaje
        result = classification_service.process_message(text, phone_number, patient_id)
        
        return jsonify({"status": "success", "result": result}), 200
    
    except Exception as e:
        logger.error(f"Error procesando mensaje de Twilio: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def process_messagebird_message(data):
    """Procesa mensajes del formato de MessageBird"""
    try:
        # Estructura de MessageBird
        message = data.get('message', {})
        message_id = message.get('id', '')
        text = message.get('payload', {}).get('text', '')
        phone_number = message.get('originator', '')
        
        # Buscar cuidador y paciente asociado
        patient_id = find_patient_by_caregiver(phone_number)
        
        # Procesar el mensaje
        result = classification_service.process_message(text, phone_number, patient_id)
        
        return jsonify({"status": "success", "result": result}), 200
    
    except Exception as e:
        logger.error(f"Error procesando mensaje de MessageBird: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
    

def process_generic_message(data):
    """
    Intenta procesar un mensaje cuando no se puede determinar el proveedor
    """
    try:
        logger.info("Intentando procesamiento genérico del mensaje")
        
        # Buscar texto en ubicaciones probables
        text = None
        phone_number = None
        
        # Caso 1: JSON simple con campos directos
        if "text" in data and isinstance(data["text"], str):
            text = data["text"]
        elif "message" in data and isinstance(data["message"], str):
            text = data["message"]
        elif "body" in data and isinstance(data["body"], str):
            text = data["body"]
            
        # Caso 2: JSON anidado
        if not text:
            if "message" in data and isinstance(data["message"], dict):
                message_obj = data["message"]
                if "text" in message_obj:
                    text = message_obj["text"]
                elif "body" in message_obj:
                    text = message_obj["body"]
                elif "content" in message_obj:
                    text = message_obj["content"]
                    
                # Intentar encontrar el número de teléfono
                if "from" in message_obj:
                    phone_number = message_obj["from"]
                elif "sender" in message_obj:
                    phone_number = message_obj["sender"]
                elif "phone" in message_obj:
                    phone_number = message_obj["phone"]
        
        # Buscar número de teléfono en ubicaciones probables
        if not phone_number:
            if "from" in data:
                phone_number = data["from"]
            elif "sender" in data:
                phone_number = data["sender"]
            elif "phone" in data:
                phone_number = data["phone"]
            elif "number" in data:
                phone_number = data["number"]
        
        # Si no encontramos texto o número, log error y return
        if not text:
            logger.error("No se pudo extraer el texto del mensaje")
            return jsonify({"status": "error", "message": "No se pudo extraer el texto del mensaje"}), 400
            
        if not phone_number:
            logger.warning("No se pudo extraer el número de teléfono, usando 'desconocido'")
            phone_number = "desconocido"
            
        # Buscar paciente (si tenemos número)
        patient_id = find_patient_by_caregiver(phone_number) if phone_number != "desconocido" else None
        
        # Procesar el mensaje
        result = classification_service.process_message(text, phone_number, patient_id)
        
        return jsonify({"status": "success", "result": result}), 200
        
    except Exception as e:
        logger.error(f"Error en procesamiento genérico del mensaje: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
    

def find_patient_by_caregiver(phone_number):
    """
    Busca el paciente asociado a un cuidador por su número de teléfono
    
    Args:
        phone_number (str): Número de teléfono del cuidador
        
    Returns:
        int: ID del paciente o None si no se encuentra
    """
    try:
        # Limpieza básica del número de teléfono
        phone_number = phone_number.replace('whatsapp:', '').strip()
        
        # Buscar cuidador por número de teléfono
        caregiver = Caregiver.query.filter_by(phone_number=phone_number).first()
        
        if caregiver and caregiver.patient_id:
            return caregiver.patient_id
        
        return None
    except Exception as e:
        logger.error(f"Error buscando paciente por cuidador: {e}")
        return None
    
    