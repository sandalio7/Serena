from app.extensions import db
from app.models.base import Base  # Cambiado de BaseModel a Base

class ClassifiedValue(Base):  # Cambiado de BaseModel a Base
    """
    Modelo para los valores clasificados extraídos de mensajes.
    """
    __tablename__ = 'classified_values'
    
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    value = db.Column(db.Text)
    confidence = db.Column(db.Float)
    
    # Relaciones (message se define como backref desde Message)
    
    def __repr__(self):
        return f"<ClassifiedValue id={self.id} message_id={self.message_id} subcategory_id={self.subcategory_id}>"

    @classmethod
    def get_by_message(cls, message_id):
        """
        Obtiene todos los valores clasificados para un mensaje específico.
        """
        return cls.query.filter_by(message_id=message_id).all()
    
    @classmethod
    def get_by_subcategory(cls, subcategory_id, limit=None):
        """
        Obtiene valores clasificados para una subcategoría específica,
        opcionalmente limitados a un número específico y ordenados por fecha.
        """
        query = cls.query.filter_by(subcategory_id=subcategory_id)
        query = query.join(cls.message).order_by(db.desc('messages.created_at'))
        
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    @classmethod
    def get_by_category_and_period(cls, category_id, start_date, end_date=None):
        """
        Obtiene valores clasificados para una categoría y período específicos.
        """
        from app.models.subcategory import Subcategory
        from app.models.message import Message
        
        query = cls.query.join(
            Subcategory, cls.subcategory_id == Subcategory.id
        ).join(
            Message, cls.message_id == Message.id
        ).filter(
            Subcategory.category_id == category_id,
            Message.created_at >= start_date
        )
        
        if end_date:
            query = query.filter(Message.created_at <= end_date)
            
        return query.order_by(db.desc(Message.created_at)).all()