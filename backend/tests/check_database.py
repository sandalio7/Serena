# backend/tests/check_database.py
import sys
sys.path.append('..')

from app import create_app, db
from app.models import Patient, Caregiver, Message, ClassifiedData
import json

def check_database():
    app = create_app('development')
    
    with app.app_context():
        # Verificar el último mensaje
        latest_message = Message.query.order_by(Message.id.desc()).first()
        print(f"Último mensaje ID: {latest_message.id}")
        print(f"Contenido: {latest_message.content}")
        print(f"WhatsApp ID: {latest_message.whatsapp_message_id}")
        print(f"De cuidador ID: {latest_message.caregiver_id}")
        print(f"Para paciente ID: {latest_message.patient_id}")
        print(f"Fecha: {latest_message.created_at}")
        print("-" * 50)
        
        # Verificar datos clasificados
        latest_classified = ClassifiedData.query.order_by(ClassifiedData.id.desc()).first()
        print(f"Datos clasificados ID: {latest_classified.id}")
        print(f"Raw data: {latest_classified.raw_data}")
        print(f"Resumen: {latest_classified.summary}")
        print(f"Para mensaje ID: {latest_classified.message_id}")
        print(f"Para paciente ID: {latest_classified.patient_id}")

if __name__ == "__main__":
    check_database()