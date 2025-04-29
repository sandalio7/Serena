#!/usr/bin/env python3
"""
Script para probar el webhook de WhatsApp con datos simulados.
"""

import os
import sys
import json
import requests
from pprint import pprint

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_webhook_verification():
    """Prueba la verificación del webhook"""
    print("\n=== PRUEBA DE VERIFICACIÓN DEL WEBHOOK ===")
    
    # Obtener token de verificación del .env
    from dotenv import load_dotenv
    load_dotenv()
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    
    if not verify_token:
        print("❌ No se encontró WHATSAPP_VERIFY_TOKEN en el archivo .env")
        return
    
    # URL del webhook (asegúrate de que la aplicación Flask esté en ejecución)
    base_url = "http://localhost:5000"
    webhook_url = f"{base_url}/api/webhook/whatsapp"
    
    # Parámetros de verificación
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": verify_token,
        "hub.challenge": "challenge_token_1234567890"
    }
    
    try:
        # Enviar solicitud GET para verificación
        print(f"Enviando solicitud de verificación a: {webhook_url}")
        response = requests.get(webhook_url, params=params)
        
        print(f"Código de estado: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
        if response.status_code == 200 and response.text == params["hub.challenge"]:
            print("✅ Verificación exitosa")
        else:
            print("❌ Verificación fallida")
            
    except Exception as e:
        print(f"❌ Error en la prueba de verificación: {e}")

def test_whatsapp_message_processing():
    """Prueba el procesamiento de mensajes de WhatsApp"""
    print("\n=== PRUEBA DE PROCESAMIENTO DE MENSAJES ===")
    
    # URL del webhook (asegúrate de que la aplicación Flask esté en ejecución)
    base_url = "http://localhost:5000"
    webhook_url = f"{base_url}/api/webhook/whatsapp"
    
    # Crear payload de ejemplo para WhatsApp Cloud API
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "12345678901",
                                "phone_number_id": "12345678901"
                            },
                            "messages": [
                                {
                                    "id": "wamid.abcdefg123456789",
                                    "from": "9876543210",
                                    "timestamp": "1679123456",
                                    "type": "text",
                                    "text": {
                                        "body": "Hoy María estuvo un poco mejor. Caminó unos 100 pasos hasta el jardín y comió bien el almuerzo. Sigue olvidando tomar su medicamento para la presión, tuve que recordárselo tres veces. Gastamos 45€ en medicinas."
                                    }
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    try:
        # Enviar solicitud POST con el mensaje simulado
        print(f"Enviando mensaje simulado a: {webhook_url}")
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=payload, headers=headers)
        
        print(f"Código de estado: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Mensaje procesado correctamente")
            print("\nRespuesta del servidor:")
            pprint(response.json())
        else:
            print("❌ Error procesando el mensaje")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la prueba de mensaje: {e}")

def test_twilio_message_processing():
    """Prueba el procesamiento de mensajes de Twilio"""
    print("\n=== PRUEBA DE PROCESAMIENTO DE MENSAJES DE TWILIO ===")
    
    # URL del webhook (asegúrate de que la aplicación Flask esté en ejecución)
    base_url = "http://localhost:5000"
    webhook_url = f"{base_url}/api/webhook/whatsapp"
    
    # Crear payload de ejemplo para Twilio
    payload = {
        "SmsMessageSid": "SMabcdef123456789",
        "NumMedia": "0",
        "SmsSid": "SMabcdef123456789",
        "SmsStatus": "received",
        "Body": "José no pudo dormir bien anoche, estuvo inquieto. Solo tomó un vaso de leche en el desayuno y se negó a almorzar. Parece desorientado, preguntando varias veces qué día es hoy.",
        "To": "whatsapp:+12345678901",
        "NumSegments": "1",
        "MessageSid": "SMabcdef123456789",
        "AccountSid": "ACabcdef123456789",
        "From": "whatsapp:+9876543210",
        "ApiVersion": "2010-04-01"
    }
    
    try:
        # Enviar solicitud POST con el mensaje simulado de Twilio
        print(f"Enviando mensaje simulado de Twilio a: {webhook_url}")
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TwilioProxy/1.1'
        }
        response = requests.post(webhook_url, json=payload, headers=headers)
        
        print(f"Código de estado: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Mensaje de Twilio procesado correctamente")
            print("\nRespuesta del servidor:")
            pprint(response.json())
        else:
            print("❌ Error procesando el mensaje de Twilio")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la prueba de mensaje de Twilio: {e}")

if __name__ == "__main__":
    # Asegúrate de que la aplicación Flask esté en ejecución antes de ejecutar estas pruebas
    print("IMPORTANTE: Asegúrate de que la aplicación Flask esté en ejecución en http://localhost:5000")
    print("Puedes iniciarla con: python run.py")
    
    input("Presiona Enter para continuar con las pruebas...")
    
    # Ejecutar pruebas
    test_webhook_verification()
    test_whatsapp_message_processing()
    test_twilio_message_processing()