# backend/app/models/caregiver.py
from .base import Base, db

class Caregiver(Base):
    """Modelo para representar a un cuidador"""
    __tablename__ = 'caregivers'
    
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True)  # Número de WhatsApp
    email = db.Column(db.String(100))
    role = db.Column(db.String(50))  # Rol: profesional, familiar, etc.
    
    # Relaciones
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    messages = db.relationship('Message', backref='caregiver', lazy=True)
    
    def __repr__(self):
        return f"<Caregiver {self.name}>"
    
    @staticmethod
    def get_by_phone(phone):
        """Obtener cuidador por número de teléfono"""
        return Caregiver.query.filter_by(phone=phone).first()