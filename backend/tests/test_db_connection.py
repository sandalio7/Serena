# backend/tests/test_db_connection.py
import unittest
from app import create_app, db
from app.models.patient import Patient

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_db_connection(self):
        """Verificar que podemos conectarnos a la BD y realizar operaciones CRUD"""
        # Crear un nuevo paciente
        test_patient = Patient(name="Paciente de prueba", age=75)
        db.session.add(test_patient)
        db.session.commit()
        
        # Recuperar el paciente
        patient = Patient.query.filter_by(name="Paciente de prueba").first()
        self.assertIsNotNone(patient)
        self.assertEqual(patient.name, "Paciente de prueba")
        self.assertEqual(patient.age, 75)
        
        # Actualizar el paciente
        patient.age = 76
        db.session.commit()
        updated_patient = Patient.query.filter_by(name="Paciente de prueba").first()
        self.assertEqual(updated_patient.age, 76)
        
        # Eliminar el paciente
        db.session.delete(patient)
        db.session.commit()
        deleted_patient = Patient.query.filter_by(name="Paciente de prueba").first()
        self.assertIsNone(deleted_patient)
        
        print("Test de conexión a la BD exitoso - Operaciones CRUD funcionan correctamente")

if __name__ == '__main__':
    unittest.main()