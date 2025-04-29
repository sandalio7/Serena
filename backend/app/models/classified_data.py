# backend/app/models/classified_data.py
from .base import Base, db
import json

class ClassifiedData(Base):
    """Modelo para representar datos clasificados por IA"""
    __tablename__ = 'classified_data'
    
    # Campos para almacenar datos clasificados
    raw_data = db.Column(db.Text, nullable=False)  # JSON con todos los datos clasificados
    
    # Categorías principales
    physical_health = db.Column(db.Text)  # JSON con datos de salud física
    cognitive_health = db.Column(db.Text)  # JSON con datos de salud cognitiva
    emotional_state = db.Column(db.Text)  # JSON con datos de estado emocional
    medication = db.Column(db.Text)  # JSON con datos de medicación
    expenses = db.Column(db.Text)  # JSON con datos de gastos
    summary = db.Column(db.Text)  # Resumen generado por IA
    
    # Relaciones
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    def __repr__(self):
        return f"<ClassifiedData {self.id}>"
    
    @property
    def physical_health_dict(self):
        """Convertir JSON de salud física a diccionario"""
        return json.loads(self.physical_health) if self.physical_health else {}
    
    @property
    def cognitive_health_dict(self):
        """Convertir JSON de salud cognitiva a diccionario"""
        return json.loads(self.cognitive_health) if self.cognitive_health else {}
    
    @property
    def emotional_state_dict(self):
        """Convertir JSON de estado emocional a diccionario"""
        return json.loads(self.emotional_state) if self.emotional_state else {}
    
    @property
    def medication_dict(self):
        """Convertir JSON de medicación a diccionario"""
        return json.loads(self.medication) if self.medication else {}
    
    @property
    def expenses_dict(self):
        """Convertir JSON de gastos a diccionario"""
        return json.loads(self.expenses) if self.expenses else {}
    
    @staticmethod
    def get_by_patient(patient_id, limit=10):
        """Obtener datos clasificados por paciente, ordenados por fecha"""
        return ClassifiedData.query.filter_by(patient_id=patient_id).order_by(ClassifiedData.created_at.desc()).limit(limit).all()