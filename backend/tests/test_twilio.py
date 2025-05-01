# backend/test/test_twilio_connection.py
import os
import sys
from dotenv import load_dotenv

# Añadir el directorio 'backend' al path para que Python pueda encontrar el módulo 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ahora sí podemos importar desde 'app'
from twilio.rest import Client

def test_twilio_connection():
    # Cargar variables de entorno desde el archivo .env en la carpeta backend
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)
    
    # Obtener credenciales
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    
    # Verificar que existan las credenciales
    if not account_sid or not auth_token:
        print("❌ ERROR: No se encontraron las credenciales de Twilio en el archivo .env")
        print(f"Ruta del .env buscado: {dotenv_path}")
        return False
    
    # Mostrar información (parcialmente oculta por seguridad)
    print("=== INFORMACIÓN DE CONFIGURACIÓN ===")
    print(f"Account SID: {account_sid[:6]}...{account_sid[-4:] if len(account_sid) > 10 else ''}")
    print(f"Auth Token: {auth_token[:4]}...{auth_token[-4:] if len(auth_token) > 8 else ''}")
    print(f"Número de WhatsApp: {twilio_number}")
    
    try:
        # Crear cliente Twilio
        client = Client(account_sid, auth_token)
        
        # Verificar conexión obteniendo información de la cuenta
        account_info = client.api.accounts(account_sid).fetch()
        print(f"\n✅ Conexión exitosa con Twilio!")
        print(f"Cuenta activa desde: {account_info.date_created}")
        print(f"Estado de la cuenta: {account_info.status}")
        return True
    except Exception as e:
        print(f"\n❌ Error al conectar con Twilio: {e}")
        print(f"Detalle del error: {str(e)}")
        return False

# Si estamos ejecutando este script directamente
if __name__ == "__main__":
    test_twilio_connection()