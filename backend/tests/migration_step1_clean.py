# backend/tests/migration_step1_clean.py
"""
MIGRACIÓN LIMPIA - PASO 1
Eliminar la tabla classified_data y todo su contenido
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.classified_data import ClassifiedData
import json
from datetime import datetime

def backup_classified_data():
    """
    Crear un respaldo JSON de los datos de classified_data (OPCIONAL)
    """
    print("=== RESPALDO DE DATOS (OPCIONAL) ===")
    
    try:
        records = ClassifiedData.query.all()
        
        if not records:
            print("No hay datos para respaldar en classified_data")
            return None
        
        backup_data = []
        for record in records:
            backup_data.append({
                'id': record.id,
                'message_id': record.message_id,
                'patient_id': record.patient_id,
                'raw_data': record.raw_data,
                'physical_health': record.physical_health,
                'cognitive_health': record.cognitive_health,
                'emotional_state': record.emotional_state,
                'medication': record.medication,
                'expenses': record.expenses,
                'summary': record.summary,
                'created_at': record.created_at.isoformat() if record.created_at else None,
                'updated_at': record.updated_at.isoformat() if record.updated_at else None
            })
        
        # Guardar respaldo
        backup_filename = f"classified_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = os.path.join('tests', backup_filename)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Respaldo creado: {backup_path}")
        print(f"📊 Registros respaldados: {len(backup_data)}")
        
        return backup_path
        
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return None

def drop_classified_data_table():
    """
    Eliminar la tabla classified_data completamente
    """
    print("\n=== ELIMINACIÓN DE TABLA classified_data ===")
    
    try:
        from sqlalchemy import inspect, text
        
        # Crear inspector para verificar tablas
        inspector = inspect(db.engine)
        
        # Verificar si la tabla existe
        if 'classified_data' in inspector.get_table_names():
            print("📋 Tabla classified_data encontrada")
            
            # Contar registros antes de eliminar
            try:
                count = ClassifiedData.query.count()
                print(f"📊 Registros a eliminar: {count}")
            except Exception as e:
                print(f"⚠️  No se pudo contar registros: {e}")
            
            # Eliminar la tabla
            print("🗑️  Eliminando tabla classified_data...")
            
            with db.engine.connect() as connection:
                connection.execute(text('DROP TABLE classified_data CASCADE'))
                connection.commit()
            
            print("✅ Tabla classified_data eliminada exitosamente")
            
            # Verificar que se eliminó
            inspector = inspect(db.engine)  # Recrear inspector
            if 'classified_data' not in inspector.get_table_names():
                print("✅ Verificación: Tabla eliminada correctamente")
            else:
                print("❌ Error: La tabla aún existe")
                return False
                
        else:
            print("⚠️  Tabla classified_data no existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error eliminando tabla: {e}")
        return False

def verify_new_structure():
    """
    Verificar que la nueva estructura sigue funcionando
    """
    print("\n=== VERIFICACIÓN DE NUEVA ESTRUCTURA ===")
    
    try:
        from app.models.classified_value import ClassifiedValue
        from app.models.category import Category
        from app.models.subcategory import Subcategory
        from app.models.message import Message
        from sqlalchemy import inspect
        
        # Crear inspector para verificar tablas
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # Verificar que las tablas nuevas existen
        tables_to_check = [
            ('classified_values', ClassifiedValue),
            ('categories', Category),
            ('subcategories', Subcategory),
            ('messages', Message)
        ]
        
        for table_name, model_class in tables_to_check:
            if table_name in existing_tables:
                try:
                    count = model_class.query.count()
                    print(f"✅ {table_name}: {count} registros")
                except Exception as e:
                    print(f"⚠️  {table_name}: Existe pero error contando: {e}")
            else:
                print(f"❌ {table_name}: No existe")
                return False
        
        print("✅ Nueva estructura verificada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando nueva estructura: {e}")
        return False

def main():
    """
    Función principal de migración - Paso 1
    """
    print("MIGRACIÓN LIMPIA - PASO 1: ELIMINAR classified_data")
    print("="*60)
    
    # Paso 1a: Respaldo (opcional)
    print("\n¿Deseas crear un respaldo de los datos actuales? (y/n): ", end="")
    backup_choice = input().lower().strip()
    
    backup_path = None
    if backup_choice in ['y', 'yes', 's', 'si']:
        backup_path = backup_classified_data()
        if not backup_path:
            print("❌ Error en el respaldo. ¿Continuar sin respaldo? (y/n): ", end="")
            continue_choice = input().lower().strip()
            if continue_choice not in ['y', 'yes', 's', 'si']:
                print("❌ Migración cancelada")
                return False
    
    # Paso 1b: Confirmar eliminación
    print(f"\n⚠️  ATENCIÓN: Vas a eliminar PERMANENTEMENTE la tabla classified_data")
    print("Esto eliminará todos los datos de la estructura antigua.")
    print("¿Estás seguro? Escribe 'ELIMINAR' para confirmar: ", end="")
    
    confirmation = input().strip()
    if confirmation != 'ELIMINAR':
        print("❌ Migración cancelada por seguridad")
        return False
    
    # Paso 1c: Eliminar tabla
    if not drop_classified_data_table():
        print("❌ Error eliminando tabla. Migración detenida.")
        return False
    
    # Paso 1d: Verificar nueva estructura
    if not verify_new_structure():
        print("❌ Error en nueva estructura. Revisar antes de continuar.")
        return False
    
    print("\n" + "="*60)
    print("✅ PASO 1 COMPLETADO EXITOSAMENTE")
    print("✅ Tabla classified_data eliminada")
    print("✅ Nueva estructura verificada")
    if backup_path:
        print(f"✅ Respaldo guardado en: {backup_path}")
    
    print("\n🚀 SIGUIENTE PASO:")
    print("   Paso 2: Actualizar classification_service.py")
    print("   - Eliminar código de classified_data")
    print("   - Usar solo classified_values")
    
    return True

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        success = main()
        if not success:
            print("\n❌ Migración fallida en Paso 1")
            exit(1)
        else:
            print("\n✅ Listo para Paso 2 - Confirma que todo funcionó antes de continuar")