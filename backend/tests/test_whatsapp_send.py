# backend/tests/test_whatsapp_send_debug.py
import os
import sys
from dotenv import load_dotenv

# Añadir el directorio 'backend' al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.whatsapp_service import WhatsAppService

def test_whatsapp_send_debug():
    # Cargar variables de entorno
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)
    
    # Mostrar información de configuración
    twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    
    print("=== PRUEBA DE ENVÍO DE MENSAJE WHATSAPP (DEBUG) ===")
    print(f"Número de WhatsApp de Twilio: {twilio_number}")
    
    # Comprobar formato
    if not twilio_number.startswith("+"):
        print("⚠️ ADVERTENCIA: El número de Twilio no comienza con '+'. Debe tener formato internacional.")
    
    # Asegurarse que estamos usando el número de WhatsApp Sandbox de Twilio
    if not twilio_number in ["+14155238886", "+12183665325"]:
        print("⚠️ ADVERTENCIA: El número no parece ser uno de los números típicos del Sandbox de WhatsApp.")
        print("Los números comunes del Sandbox de WhatsApp incluyen: +14155238886, +12183665325")
        print("Verifica en tu consola de Twilio el número correcto.")
    
    # Crear instancia del servicio
    whatsapp_service = WhatsAppService()
    
    # Número al que enviaremos el mensaje
    your_number = input("Ingresa tu número de WhatsApp (formato: +34612345678): ")
    
    # Para fines de diagnóstico, mostremos cómo se forman las URLs
    from_whatsapp = f"whatsapp:{twilio_number}"
    to_whatsapp = f"whatsapp:{your_number}"
    
    print(f"\nProbando envío con los siguientes datos:")
    print(f"Desde: {from_whatsapp}")
    print(f"Hacia: {to_whatsapp}")
    print(f"Mensaje: '¡Hola! Este es un mensaje de prueba desde Serena.'")
    
    # Confirmar si desea continuar
    confirm = input("\n¿Los datos son correctos? ¿Deseas continuar con el envío? (s/n): ")
    if confirm.lower() != 's':
        print("Prueba cancelada.")
        return False
    
    # Intentar enviar el mensaje
    result = whatsapp_service.send_message(your_number, "¡Hola! Este es un mensaje de prueba desde Serena.")
    
    if result:
        print(f"\n✅ Mensaje enviado correctamente!")
        print(f"SID del mensaje: {result.sid}")
        print(f"Estado: {result.status}")
        return True
    else:
        print("❌ Error al enviar el mensaje.")
        return False

if __name__ == "__main__":
    test_whatsapp_send_debug()