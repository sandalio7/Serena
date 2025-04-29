# backend/app/models/patient.py
from .base import Base, db

class Patient(Base):
    """Modelo para representar a un paciente"""
    __tablename__ = 'patients'
    
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    conditions = db.Column(db.String(255))  # Condiciones médicas
    notes = db.Column(db.Text)
    
    # Relaciones
    caregivers = db.relationship('Caregiver', backref='patient', lazy=True)
    messages = db.relationship('Message', backref='patient', lazy=True)
    classified_data = db.relationship('ClassifiedData', backref='patient', lazy=True)
    
    def __repr__(self):
        return f"<Patient {self.name}>"
    
    @staticmethod
    def get_all():
        """Obtener todos los pacientes"""
        return Patient.query.all()
    
    @staticmethod
    def get_by_id(patient_id):
        """Obtener paciente por ID"""
        return Patient.query.get(patient_id)