# diagnostic_db.py (para guardar en /backend/tests/)
import os
from pathlib import Path
import sqlite3

# Obtener la ruta absoluta ajustada para ejecutarse desde /backend/tests/
base_dir = Path(__file__).parent.parent.absolute()  # Subir un nivel desde tests/
instance_dir = base_dir / "instance"
db_path = instance_dir / "serena.db"

print("-" * 50)
print("DIAGNÓSTICO DE CONEXIÓN SQLITE")
print("-" * 50)
print(f"Directorio base: {base_dir}")
print(f"Directorio instance: {instance_dir}")
print(f"Ruta de la BD: {db_path}")
print("-" * 50)

# Verificar si el directorio instance existe
if not instance_dir.exists():
    print("El directorio 'instance' no existe. Creándolo...")
    instance_dir.mkdir(parents=True, exist_ok=True)
    print(f"Directorio creado: {instance_dir}")

# Verificar si el archivo de la BD existe
if db_path.exists():
    print(f"La base de datos existe en: {db_path}")
    print(f"Tamaño del archivo: {db_path.stat().st_size} bytes")
    print(f"Permisos: {oct(db_path.stat().st_mode)[-3:]}")
else:
    print("El archivo de base de datos no existe. Intentando crearlo...")

# Intentar conectar a la BD
try:
    print("\nProbando conexión a la base de datos...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ejecutar una consulta simple
    cursor.execute("PRAGMA table_info(sqlite_master)")
    tables = cursor.fetchall()
    print("Conexión exitosa!")
    
    # Verificar si podemos escribir
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY)")
        conn.commit()
        print("Escritura exitosa en la BD")
        
        # Limpiar tabla de prueba
        cursor.execute("DROP TABLE IF EXISTS test_table")
        conn.commit()
    except Exception as e:
        print(f"Error al escribir en la BD: {e}")
    
    conn.close()
    
except Exception as e:
    print(f"Error al conectar a la BD: {e}")
    
# Modificación recomendada para config.py
print("\nRecomendación para config.py:")
print("""
# Usar ruta absoluta para la BD
basedir = Path(__file__).parent.parent.absolute()
instance_dir = basedir / "instance"
instance_dir.mkdir(parents=True, exist_ok=True)  # Asegurar que el directorio existe
db_path = instance_dir / "serena.db"

class Config:
    # Resto del código...
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path.absolute()}'
""")

print("\nRecomendación para __init__.py:")
print("""
def create_app(config_name='default'):
    # Crear la aplicación Flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Asegurar que el directorio instance existe
    instance_dir = Path(app.root_path).parent / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)
    
    # Inicializar extensiones
    db.init_app(app)
    # Resto del código...
""")