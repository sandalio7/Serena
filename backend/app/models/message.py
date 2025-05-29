# backend/app/models/message.py
from .base import Base, db

class Message(Base):
    """Modelo para representar mensajes recibidos de WhatsApp"""
    __tablename__ = 'messages'
    
    content = db.Column(db.Text, nullable=False)  # Contenido del mensaje
    whatsapp_message_id = db.Column(db.String(100), unique=True)  # ID del mensaje en WhatsApp
    
    # Relaciones
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregivers.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    classified_data = db.relationship('ClassifiedData', backref='message', uselist=False)
    # Nueva relación con ClassifiedValue
    classified_values = db.relationship('ClassifiedValue', backref='message', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Message {self.id}>"