from flask import Flask
from .config import config
from .extensions import db, migrate, cors
from pathlib import Path

def create_app(config_name='default'):
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Asegurar que el directorio instance existe
    instance_dir = Path(app.root_path).parent / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Verificar conexión a la BD
    with app.app_context():
        try:
            db.engine.connect()
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