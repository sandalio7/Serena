# backend/tests/insert_test_data.py
import sys
sys.path.append('..')  # Para poder importar desde el directorio padre

from app import create_app, db
from app.models import Patient, Caregiver, Message, ClassifiedData
from datetime import datetime
import json

def create_test_data():
    app = create_app('development')
    
    with app.app_context():
        try:
            # Verificar si ya hay pacientes
            existing_patients = Patient.query.count()
            
            if existing_patients > 0:
                print(f"Ya hay {existing_patients} pacientes en la base de datos.")
                # Obtener el primer paciente para ejemplo
                patient = Patient.query.first()
                print(f"Usando paciente existente: {patient.name}")
            else:
                # Crear un paciente de prueba solo si no existe ninguno
                patient = Patient(
                    name="María García",
                    age=78,
                    conditions=["Alzheimer inicial", "hipertensión"],
                    notes="Paciente requiere monitoreo diario de presión arterial"
                )
                db.session.add(patient)
                db.session.commit()
                print(f"✅ Paciente creado: {patient.name}")
            
            # Verificar si ya hay cuidadores
            existing_caregivers = Caregiver.query.count()
            
            if existing_caregivers > 0:
                print(f"Ya hay {existing_caregivers} cuidadores en la base de datos.")
                caregiver1 = Caregiver.query.first()
                caregiver2 = Caregiver.query.filter_by(id=2).first() if Caregiver.query.count() > 1 else caregiver1
                print(f"Usando cuidadores existentes: {caregiver1.name}, {caregiver2.name}")
            else:
                # Crear cuidadores
                caregiver1 = Caregiver(
                    name="Ana Pérez",
                    phone="+1234567890",
                    email="ana@example.com",
                    patient_id=patient.id
                )
                
                caregiver2 = Caregiver(
                    name="Juan Rodríguez",  
                    phone="+0987654321",
                    email="juan@example.com",
                    patient_id=patient.id
                )
                
                db.session.add_all([caregiver1, caregiver2])
                db.session.commit()
                print(f"✅ Cuidadores creados: {caregiver1.name}, {caregiver2.name}")
            
            # Verificar si ya hay mensajes
            existing_messages = Message.query.count()
            
            if existing_messages > 0:
                print(f"Ya hay {existing_messages} mensajes en la base de datos.")
                print("Usando mensajes existentes para datos clasificados...")
                # Obtener los últimos 2 mensajes
                message1 = Message.query.first()
                message2 = Message.query.filter_by(id=2).first() if Message.query.count() > 1 else message1
            else:
                # Crear algunos mensajes de prueba
                message1 = Message(
                    content="Hola, María tomó sus medicamentos a las 8am y desayunó bien",
                    whatsapp_message_id="WA_001",
                    caregiver_id=caregiver1.id,
                    patient_id=patient.id,
                    created_at=datetime.now()
                )
                
                message2 = Message(
                    content="Primera revisión del día: María está de buen humor, ando_pasos_datos",
                    whatsapp_message_id="WA_002",
                    caregiver_id=caregiver1.id,
                    patient_id=patient.id,
                    created_at=datetime.now()
                )
                
                db.session.add_all([message1, message2])
                db.session.commit()
                print(f"✅ Mensajes creados: {message1.id}, {message2.id}")
            
            # Verificar si ya hay datos clasificados
            existing_classified = ClassifiedData.query.count()
            
            if existing_classified > 0:
                print(f"Ya hay {existing_classified} datos clasificados en la base de datos.")
            else:
                # Crear datos clasificados de prueba
                raw_data = {
                    "medication": {"adherence": True, "efficacy": "good", "notes": "Tomó medicamentos según horario"},
                    "mood": "good",
                    "physical_state": "stable",
                    "summary": "Cumplimiento de medicación y estado estable"
                }
                
                classified_data1 = ClassifiedData(
                    raw_data=json.dumps(raw_data),  # Todo el JSON como string
                    physical_health=json.dumps({"state": "stable", "notes": "No presenta síntomas"}),
                    cognitive_health=None,
                    emotional_state=json.dumps({"mood": "good", "social_interaction": "normal"}),
                    medication=json.dumps({"adherence": True, "efficacy": "good"}),
                    expenses=None,
                    summary="Cumplimiento de medicación y estado estable",
                    message_id=message1.id,
                    patient_id=patient.id
                )
                
                db.session.add(classified_data1)
                db.session.commit()
                print(f"✅ Datos clasificados creados para mensaje {message1.id}")
            
            print("\n✅ Todos los datos de prueba verificados/creados exitosamente!")
            print(f"Paciente ID: {patient.id}")
            print(f"Cuidadores IDs: {caregiver1.id}, {caregiver2.id}")
            
        except Exception as e:
            print(f"❌ Error al crear datos de prueba: {e}")
            db.session.rollback()

if __name__ == "__main__":
    create_test_data()