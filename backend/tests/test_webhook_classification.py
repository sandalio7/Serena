# backend/tests/test_webhook_classification.py
import json
import unittest
import os
import sys

# Agregar el directorio padre al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.patient import Patient
from app.models.caregiver import Caregiver
from app.models.message import Message
from app.models.classified_data import ClassifiedData
from app.services.classification_service import ClassificationService

class TestWebhookClassification(unittest.TestCase):
    def setUp(self):
        # Crear la aplicación en modo testing
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Crear tablas y datos de prueba
        db.create_all()
        self._create_test_data()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _create_test_data(self):
        # Crear paciente de prueba
        patient = Patient(
            name="María García",
            age=78,
            conditions="Alzheimer inicial, hipertensión"
        )
        db.session.add(patient)
        db.session.commit()
        
        # Crear cuidador de prueba
        caregiver = Caregiver(
            name="Ana Pérez",
            phone="+1234567890",
            role="Profesional",
            patient_id=patient.id
        )
        db.session.add(caregiver)
        db.session.commit()
        
        self.patient_id = patient.id
        self.caregiver_id = caregiver.id
    
    def test_classification_service(self):
        """Probar que el servicio de clasificación funciona correctamente"""
        classification_service = ClassificationService()
        test_message = "María durmió bien anoche. Desayunó con apetito y caminó 15 minutos en el jardín. Sigue olvidando tomar su medicamento para la presión, tuve que recordárselo dos veces. Gastamos 45€ en medicinas."
        
        # Crear mensaje en la BD
        message = Message(
            content=test_message,
            whatsapp_message_id="test_msg_123",
            caregiver_id=self.caregiver_id,
            patient_id=self.patient_id
        )
        db.session.add(message)
        db.session.commit()
        
        # Clasificar mensaje usando el servicio de Gemini
        classification_result = classification_service.gemini_service.classify_message(test_message)
        
        # Verificar que el resultado tiene la estructura esperada
        self.assertIsNotNone(classification_result)
        self.assertIn('categorias', classification_result)
        self.assertIn('resumen', classification_result)
        
        print("\nResultado de clasificación:")
        print(json.dumps(classification_result, indent=2, ensure_ascii=False))
        
        # Guardar clasificación
        classification_service._save_classification_data(
            message_id=message.id,
            classification_data=classification_result,
            patient_id=self.patient_id
        )
        
        # Verificar que se guardó correctamente en la BD
        classified_data = ClassifiedData.query.filter_by(message_id=message.id).first()
        self.assertIsNotNone(classified_data)
        self.assertIsNotNone(classified_data.raw_data)
        self.assertIsNotNone(classified_data.summary)
        
        print("\nDatos clasificados guardados correctamente en la BD")
    
    def test_twilio_webhook_integration(self):
        """Probar que el webhook de Twilio procesa correctamente los mensajes"""
        # Simular payload de Twilio
        twilio_payload = {
            "SmsMessageSid": "SM123456789",
            "NumMedia": "0",
            "SmsSid": "SM123456789",
            "SmsStatus": "received",
            "Body": "María durmió bien anoche. Hoy está animada y comió bien.",
            "From": "+1234567890",
            "AccountSid": "AC123456789",
            "To": "+0987654321",
            "MessageSid": "SM123456789"
        }
        
        # Enviar solicitud POST al webhook
        response = self.client.post(
            '/api/webhook/whatsapp',
            data=twilio_payload,
            content_type='application/x-www-form-urlencoded'
        )
        
        # Verificar respuesta del webhook
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el mensaje se guardó en la BD
        message = Message.query.filter_by(whatsapp_message_id="SM123456789").first()
        self.assertIsNotNone(message)
        self.assertEqual(message.content, "María durmió bien anoche. Hoy está animada y comió bien.")
        
        # Verificar que se generó una clasificación
        classified_data = ClassifiedData.query.filter_by(message_id=message.id).first()
        self.assertIsNotNone(classified_data)
        
        print("\nPrueba de webhook completada - Mensaje procesado y clasificado correctamente")

if __name__ == '__main__':
    unittest.main()