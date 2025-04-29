# backend/tests/test_webhooks.py
import json
import pytest
from unittest.mock import patch
from app.services.classification_service import process_whatsapp_message

def test_webhook_verification(client, app):
    """Probar la verificación del webhook de WhatsApp"""
    # Simular petición de verificación
    with app.app_context():
        with patch('os.environ.get') as mock_get:
            mock_get.return_value = 'test-token'
            
            response = client.get('/api/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=test-token&hub.challenge=challenge-code')
            
            assert response.status_code == 200
            assert response.data.decode('utf-8') == 'challenge-code'
            
            # Probar con token incorrecto
            response = client.get('/api/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=wrong-token&hub.challenge=challenge-code')
            assert response.status_code == 403

def test_whatsapp_message_processing(client, app):
    """Probar el procesamiento de mensajes de WhatsApp"""
    # Ejemplo de payload de WhatsApp (simplificado)
    whatsapp_payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "id": "test-msg-id-123",
                        "from": "+1234567890",
                        "text": {
                            "body": "Paciente durmió bien hoy. Tomó todos sus medicamentos."
                        }
                    }]
                }
            }]
        }]
    }
    
    with app.app_context():
        # Usar mock para evitar llamadas reales a Gemini AI
        with patch('app.services.gemini_service.classify_message') as mock_classify:
            mock_classify.return_value = {
                "categorias": [
                    {
                        "nombre": "Salud Física",
                        "detectada": True,
                        "subcategorias": [
                            {
                                "nombre": "Sueño",
                                "detectada": True,
                                "valor": "durmió bien hoy",
                                "confianza": 0.9
                            }
                        ]
                    },
                    {
                        "nombre": "Medicación",
                        "detectada": True,
                        "subcategorias": [
                            {
                                "nombre": "Adherencia",
                                "detectada": True,
                                "valor": "Tomó todos sus medicamentos",
                                "confianza": 0.95
                            }
                        ]
                    }
                ],
                "resumen": "El paciente descansó bien y cumplió con su medicación."
            }
            
            response = client.post(
                '/api/webhook/whatsapp',
                json=whatsapp_payload,
                content_type='application/json'
            )
            
            # Verificar respuesta
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'