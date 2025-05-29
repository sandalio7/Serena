from app.extensions import db
from app.models.base import Base  # Cambiado de BaseModel a Base

class Subcategory(Base):  # Cambiado de BaseModel a Base
    """
    Modelo para las subcategorías de clasificación.
    """
    __tablename__ = 'subcategories'
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer)
    
    # Relaciones
    classified_values = db.relationship('ClassifiedValue', backref='subcategory', lazy=True)
    
    def __repr__(self):
        return f"<Subcategory id={self.id} name={self.name} category_id={self.category_id}>"

    @classmethod
    def get_by_category(cls, category_id):
        """
        Obtiene todas las subcategorías activas para una categoría específica.
        """
        return cls.query.filter_by(
            category_id=category_id, 
            active=True
        ).order_by(cls.display_order).all()
    
    @classmethod
    def get_all_active(cls):
        """
        Obtiene todas las subcategorías activas ordenadas por categoría y orden de visualización.
        """
        return cls.query.filter_by(
            active=True
        ).order_by(cls.category_id, cls.display_order).all()