# backend/run.py
import os
from app import create_app, db
from sqlalchemy import text

# Determinar entorno desde variable de entorno o usar default
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Probar conexión y crear tablas antes de iniciar el servidor
    with app.app_context():
        try:
            # Probar conexión a PostgreSQL
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("✅ Conexión exitosa a PostgreSQL")
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Confirmar las tablas creadas
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
                tables = [row[0] for row in result]
                print(f"✅ Tablas disponibles: {tables}")
            
        except Exception as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            print("Asegúrate de que PostgreSQL esté corriendo:")
            print("  docker compose up -d postgres")
            exit(1)
    
    # Determinar puerto desde variable de entorno o usar default (5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)