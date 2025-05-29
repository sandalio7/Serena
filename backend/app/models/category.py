from app.extensions import db
from app.models.base import Base  # Cambiado de BaseModel a Base

class Category(Base):  # Cambiado de BaseModel a Base
    """
    Modelo para las categorías principales de clasificación.
    """
    __tablename__ = 'categories'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer)
    
    # Relaciones
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)
    
    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"

    @classmethod
    def get_all_active(cls):
        """
        Obtiene todas las categorías activas ordenadas por display_order.
        """
        return cls.query.filter_by(active=True).order_by(cls.display_order).all()