# backend/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la ruta base del proyecto
basedir = Path(__file__).parent.parent.absolute()
instance_dir = basedir / "instance"
# Asegurar que el directorio instance existe
instance_dir.mkdir(parents=True, exist_ok=True)
db_path = instance_dir / "serena.db"

class Config:
    """Configuración base para la aplicación Flask"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-insegura-cambiar'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path.absolute()}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True
    
class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    # Usar la ruta absoluta también para testing
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path.absolute()}'
    
class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False
    
# Mapeo de configuraciones según el entorno
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}