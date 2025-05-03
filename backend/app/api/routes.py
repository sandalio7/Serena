# backend/app/api/routes.py
from flask import Blueprint

# Importar blueprints
from .webhooks import webhook_bp
from .patient_data import patient_bp
from .financial_data import financial_bp  # Importar blueprint financiero
from .health_data import health_bp  # Importar blueprint de salud

def init_routes(app):
    """Inicializar y registrar todos los blueprints"""
    
    # Registrar blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(financial_bp)  # Registrar blueprint financiero
    app.register_blueprint(health_bp)  # Registrar blueprint de salud
    
    # Ruta de verificación de estado
    @app.route('/api/health-check', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'Serena API está funcionando correctamente'}
    
    # Ruta de prueba para verificar que la función init_routes está siendo llamada
    @app.route('/api/test', methods=['GET'])
    def test_api():
        return {'status': 'success', 'message': 'API routes initialized successfully'}