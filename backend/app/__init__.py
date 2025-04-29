# backend/app/__init__.py
from flask import Flask
from .config import config
from .extensions import db, migrate, cors

def create_app(config_name='default'):
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Importar e inicializar blueprints
    from .api.routes import init_routes
    init_routes(app)
    
    # Registrar handlers
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """Registrar manejadores de errores"""
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Internal server error'}, 500