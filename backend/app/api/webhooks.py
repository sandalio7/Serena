#backend/app/api/webhooks.py
import os
import logging
from flask import Blueprint, request, jsonify
from app.services.classification_service import ClassificationService
from app.models.caregiver import Caregiver
from app.models.message import Message
from app.extensions import db

# Configuración de logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializar Blueprint
webhook_bp = Blueprint('webhooks', __name__, url_prefix='/api/webhook')

# Token de verificación para el webhook
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
if not VERIFY_TOKEN:
    logger.warning("WHATSAPP_VERIFY_TOKEN no configurado en .env. Usando token predeterminado.")
    VERIFY_TOKEN = "serena-secret-key"  # Token predeterminado solo como fallback

# Inicializar servicio de clasificación
classification_service = ClassificationService()

@webhook_bp.route("/test", methods=["GET"])
def test_webhook():
    """Ruta de prueba para verificar que el blueprint está registrado"""
    return jsonify({"status": "success", "message": "Webhook blueprint is working"}), 200

@webhook_bp.route("/whatsapp", methods=["GET", "POST"])
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
        try:
            # Detectar tipo de proveedor primero
            provider_type = detect_provider(request)
            logger.info(f"Proveedor detectado: {provider_type}")
            
            # Obtener los datos según el tipo de proveedor
            if provider_type == "twilio" and request.form:
                data = request.form.to_dict()
                logger.info(f"Datos de formulario recibidos: {data}")
                return process_twilio_message(data)
            elif request.is_json:
                data = request.get_json(silent=True)
                
                if not data:
                    logger.error("No se encontraron datos JSON o formulario válidos")
                    return jsonify({"status": "error", "message": "No data provided"}), 400
                
                if provider_type == "whatsapp_cloud":
                    return process_whatsapp_cloud_message(data)
                elif provider_type == "twilio":
                    return process_twilio_message(data)
                elif provider_type == "messagebird":
                    return process_messagebird_message(data)
            
            # Si no se pudo determinar el proveedor o no hay datos válidos
            logger.warning("Formato de datos no reconocido, intentando procesamiento genérico")
            
            # Intentar obtener datos de cualquier fuente
            data = {}
            if request.form:
                data = request.form.to_dict()
            elif request.is_json:
                data = request.get_json(silent=True) or {}
            
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
    
    if "twilio" in user_agent:
        return "twilio"
    elif "messagebird" in user_agent:
        return "messagebird"
    
    # Si no se detecta por headers, intentar por el formato de los datos
    # Para form-data (application/x-www-form-urlencoded) como envía Twilio
    if request.form:
        data = request.form.to_dict()
        if "SmsMessageSid" in data or "MessageSid" in data:
            return "twilio"
    
    # Para JSON (application/json)
    if request.is_json:
        data = request.get_json(silent=True)
        if not data:
            return "unknown"
        
        # WhatsApp Cloud API format detection
        if "object" in data and data.get("object") == "whatsapp_business_account":
            return "whatsapp_cloud"
        # Twilio format detection en JSON (menos común)
        elif "SmsMessageSid" in data:
            return "twilio"
        # MessageBird format detection
        elif "message" in data and "originator" in data.get("message", {}):
            return "messagebird"
    
    # Default
    return "unknown"

def process_twilio_message(data):
    """
    Procesa un mensaje recibido a través de Twilio
    """
    logger.info(f"Procesando mensaje de Twilio: {data}")
    
    try:
        # Extraer información del mensaje
        sender = data.get('From', '')
        body = data.get('Body', '')
        message_sid = data.get('MessageSid', '')
        
        # Eliminar el prefijo 'whatsapp:' si existe
        if sender and sender.startswith('whatsapp:'):
            sender = sender[9:]
        
        logger.info(f"Mensaje de WhatsApp recibido: De: {sender}, Contenido: {body}")
        
        # Buscar al cuidador en la base de datos
        caregiver = Caregiver.query.filter_by(phone=sender).first()
        
        if not caregiver:
            logger.warning(f"Cuidador no encontrado para el número: {sender}")
            # Podríamos crear un cuidador temporal o rechazar el mensaje
            return jsonify({
                "status": "error", 
                "message": "Cuidador no registrado"
            }), 400
        
        # Clasificar y procesar el mensaje
        if body:
            try:
                # Crear nuevo mensaje en la BD
                message = Message(
                    content=body,
                    whatsapp_message_id=message_sid,
                    caregiver_id=caregiver.id,
                    patient_id=caregiver.patient_id
                )
                db.session.add(message)
                db.session.commit()
                
                logger.info(f"Mensaje guardado con ID: {message.id}")
                
                # Clasificar el mensaje usando el servicio de IA
                classification_result = classification_service.gemini_service.classify_message(body)
                
                # Guardar los datos clasificados
                classification_service._save_classification_data(message.id, classification_result, caregiver.patient_id)
                
                logger.info(f"Mensaje clasificado y guardado correctamente")
                return jsonify({"status": "success", "message": "Mensaje procesado y clasificado"}), 200
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error procesando mensaje: {e}")
                return jsonify({"status": "error", "message": f"Error en procesamiento: {str(e)}"}), 500
        else:
            logger.warning("Mensaje recibido sin contenido")
            return jsonify({"status": "error", "message": "Mensaje sin contenido"}), 400
    
    except Exception as e:
        logger.error(f"Error procesando mensaje de Twilio: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def process_whatsapp_cloud_message(data):
    """
    Procesa un mensaje recibido directamente a través de WhatsApp Cloud API
    """
    logger.info(f"Procesando mensaje de WhatsApp Cloud API (no implementado aún)")
    return jsonify({"status": "not_implemented", "message": "WhatsApp Cloud API processing not implemented yet"}), 200

def process_messagebird_message(data):
    """
    Procesa un mensaje recibido a través de MessageBird
    """
    logger.info(f"Procesando mensaje de MessageBird (no implementado aún)")
    return jsonify({"status": "not_implemented", "message": "MessageBird processing not implemented yet"}), 200

def process_generic_message(data):
    """
    Intenta procesar un mensaje de formato desconocido
    """
    logger.warning(f"Proveedor no reconocido. Intentando procesamiento genérico.")
    # Intenta buscar campos comunes en diferentes formatos
    sender = data.get('From') or data.get('from') or data.get('sender')
    body = data.get('Body') or data.get('body') or data.get('text') or data.get('content')
    
    if sender and body:
        logger.info(f"Mensaje genérico detectado - De: {sender}, Contenido: {body}")
        return jsonify({"status": "success", "message": "Generic message processed"}), 200
    else:
        logger.error(f"No se pudieron extraer datos básicos del mensaje")
        return jsonify({"status": "error", "message": "Could not extract message data"}), 400