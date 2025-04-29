# backend/app/api/webhooks.py
import os
from flask import Blueprint, request, jsonify

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
        
        # Verificar token
        if verify_token == os.environ.get('WHATSAPP_VERIFY_TOKEN'):
            return challenge, 200
        return 'Token de verificación inválido', 403
    
    elif request.method == 'POST':
        # Aquí implementaremos el procesamiento de mensajes entrantes
        # Por ahora, solo registraremos la recepción y devolveremos un OK
        print("Webhook de WhatsApp recibido:", request.json)
        
        # Este es un placeholder para la futura implementación completa
        return jsonify({'status': 'ok', 'message': 'Webhook recibido'}), 200