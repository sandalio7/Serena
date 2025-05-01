# En app/services/whatsapp_service.py

import os
from twilio.rest import Client

class WhatsAppService:
    def __init__(self, account_sid=None, auth_token=None, twilio_number=None):
        """
        Inicializa el servicio de WhatsApp con credenciales de Twilio
        """
        self.account_sid = account_sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = auth_token or os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = twilio_number or os.getenv("TWILIO_WHATSAPP_NUMBER")
        self.client = Client(self.account_sid, self.auth_token) if self.account_sid and self.auth_token else None
    
    def send_message(self, to_number, message_body):
        """
        Envía un mensaje de WhatsApp a través de Twilio
        
        Args:
            to_number (str): Número de WhatsApp del destinatario en formato internacional
            message_body (str): Contenido del mensaje
            
        Returns:
            message: Objeto mensaje de Twilio o None si hay error
        """
        if not self.client:
            print("Cliente Twilio no inicializado. Verifica tus credenciales.")
            return None
            
        # Aseguramos formato correcto para WhatsApp
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"
            
        from_number = f"whatsapp:{self.twilio_number}"
        
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=from_number,
                to=to_number
            )
            print(f"Mensaje enviado con SID: {message.sid}")
            return message
        except Exception as e:
            print(f"Error enviando mensaje WhatsApp: {e}")
            return None
    
    def parse_incoming_message(self, request_data):
        """
        Procesa los datos de un mensaje entrante desde Twilio
        
        Args:
            request_data (dict): Datos del webhook de Twilio
            
        Returns:
            dict: Datos estructurados del mensaje
        """
        try:
            # Obtener información relevante del mensaje
            sender = request_data.get('From', '')
            body = request_data.get('Body', '')
            media_url = request_data.get('MediaUrl0', None)
            
            # Eliminar el prefijo 'whatsapp:' si existe
            if sender and sender.startswith('whatsapp:'):
                sender = sender[9:]
                
            # Crear estructura de datos con la información del mensaje
            message_data = {
                'sender': sender,
                'body': body,
                'media_url': media_url,
                'timestamp': request_data.get('DateCreated', None),
                'message_sid': request_data.get('MessageSid', ''),
            }
            
            return message_data
            
        except Exception as e:
            print(f"Error procesando mensaje entrante: {e}")
            # Devolver diccionario vacío con estructura mínima para prevenir errores
            return {
                'sender': '',
                'body': '',
                'media_url': None,
                'timestamp': None,
                'message_sid': '',
                'error': str(e)
            }