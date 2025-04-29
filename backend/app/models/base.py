# backend/app/models/base.py
from datetime import datetime
from ..extensions import db

class Base(db.Model):
    """Modelo base con campos comunes para todos los modelos"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Guardar instancia en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Eliminar instancia de la base de datos"""
        db.session.delete(self)
        db.session.commit()