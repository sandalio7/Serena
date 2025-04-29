# backend/app/api/webhooks.py
import os
from flask import Blueprint, request, jsonify
from ..services.whatsapp_service import extract_message_from_whatsapp
from ..services.classification_service import process_whatsapp_message

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    """
    Endpoint para el webhook de WhatsApp
    
    GET: Verificación del webhook por parte de WhatsApp
    POST: Recepción de mensajes de WhatsApp
    """
    if request.method == 'GET':
        # Verificación del webhook por WhatsApp
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        print(f"Solicitud de verificación recibida: token={verify_token}")
        
        # Verificar token
        if verify_token == os.environ.get('WHATSAPP_VERIFY_TOKEN'):
            return challenge, 200
        return 'Token de verificación inválido', 403
    
    elif request.method == 'POST':
        try:
            # Obtener datos del webhook
            data = request.json
            print(f"Webhook de WhatsApp recibido: {data}")
            
            # Extraer información del mensaje
            message_text, message_id, phone_number = extract_message_from_whatsapp(data)
            
            if not message_text or not message_id or not phone_number:
                return jsonify({
                    'status': 'error',
                    'message': 'No se pudo extraer la información necesaria del mensaje'
                }), 400
            
            # Procesar el mensaje
            success, message, classified_data = process_whatsapp_message(
                message_text, message_id, phone_number
            )
            
            if not success:
                return jsonify({
                    'status': 'error',
                    'message': message
                }), 400
            
            return jsonify({
                'status': 'success',
                'message': message,
                'data': {
                    'id': classified_data.id,
                    'summary': classified_data.summary
                }
            }), 200
            
        except Exception as e:
            print(f"Error procesando webhook: {e}")
            return jsonify({
                'status': 'error',
                'message': f"Error interno: {str(e)}"
            }), 500