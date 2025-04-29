# backend/app/api/routes.py
from flask import Blueprint

# Importar blueprints
from .webhooks import webhook_bp
from .patient_data import patient_bp

def init_routes(app):
    """Inicializar y registrar todos los blueprints"""
    
    # Registrar blueprints
    app.register_blueprint(webhook_bp, url_prefix='/api/webhook')
    app.register_blueprint(patient_bp, url_prefix='/api/patients')
    
    # Ruta de verificación de estado
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'Serena API está funcionando correctamente'}