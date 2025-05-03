from flask import Flask
from .config import config
from .extensions import db, migrate, cors
from pathlib import Path

def create_app(config_name='default'):
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Asegurar que el directorio instance existe
    instance_dir = Path("C:/Users/tomas/Documents/SERENA/serena_project/backend/instance")
    instance_dir.mkdir(parents=True, exist_ok=True)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Crear tablas y datos de prueba
    with app.app_context():
        try:
            # Crear tablas
            db.create_all()
            
            # Importar modelos
            from .models.patient import Patient
            from .models.caregiver import Caregiver
            from .models.message import Message
            from .models.classified_data import ClassifiedData
            
            # Crear datos de prueba si no existen
            if not Patient.query.first():
                # Crear paciente
                patient = Patient(name="María López", age=75, conditions="Alzheimer leve")
                db.session.add(patient)
                db.session.flush()  # Para obtener el ID
                
                # Crear cuidador
                caregiver = Caregiver(
                    name="Ana Pérez",
                    phone="+5493815122808",  # Usar el número de WhatsApp real
                    patient_id=patient.id
                )
                db.session.add(caregiver)
                
                db.session.commit()
                print("Base de datos creada con datos de prueba")
            
            print("Conexión a la base de datos establecida correctamente")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
    
    # Importar e inicializar blueprints
    from .api.routes import init_routes
    init_routes(app)
    
    # Registrar handlers
    register_error_handlers(app)
    
    # Ruta de prueba
    @app.route('/test')
    def test():
        return {'message': 'Flask app is running!'}
    
    return app

def register_error_handlers(app):
    """Registrar manejadores de errores"""
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Internal server error'}, 500