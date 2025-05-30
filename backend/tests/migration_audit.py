# backend/tests/migration_audit.py
"""
Script de auditoría para verificar el estado de la migración
de classified_data a classified_values
"""

import sys
import os
# Agregar el directorio padre (backend) al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.classified_data import ClassifiedData
from app.models.classified_value import ClassifiedValue
from app.models.message import Message
from app.models.category import Category
from app.models.subcategory import Subcategory
from datetime import datetime, timedelta
import json

def audit_data_consistency():
    """
    Audita la consistencia entre la estructura antigua y nueva
    """
    print("=== AUDITORÍA DE MIGRACIÓN - PASO 1 ===\n")
    
    # 1. Contar registros en ambas estructuras
    print("1. CONTEO DE REGISTROS:")
    old_count = ClassifiedData.query.count()
    new_count = ClassifiedValue.query.count()
    message_count = Message.query.count()
    
    print(f"   - Mensajes totales: {message_count}")
    print(f"   - Registros en classified_data (estructura antigua): {old_count}")
    print(f"   - Registros en classified_values (estructura nueva): {new_count}")
    print(f"   - Ratio nuevo/antiguo: {new_count/old_count if old_count > 0 else 0:.2f}")
    print()
    
    # 2. Verificar mensajes recientes (últimos 7 días)
    print("2. MENSAJES RECIENTES (últimos 7 días):")
    week_ago = datetime.now() - timedelta(days=7)
    
    recent_messages = Message.query.filter(Message.created_at >= week_ago).all()
    recent_old_data = ClassifiedData.query.filter(ClassifiedData.created_at >= week_ago).all()
    
    recent_new_data_count = ClassifiedValue.query.join(
        Message, ClassifiedValue.message_id == Message.id
    ).filter(Message.created_at >= week_ago).count()
    
    print(f"   - Mensajes recientes: {len(recent_messages)}")
    print(f"   - Con datos en estructura antigua: {len(recent_old_data)}")
    print(f"   - Con datos en estructura nueva: {recent_new_data_count}")
    
    # Verificar si todos los mensajes recientes tienen datos en ambas estructuras
    missing_in_new = []
    for message in recent_messages:
        old_exists = any(cd.message_id == message.id for cd in recent_old_data)
        new_exists = ClassifiedValue.query.filter_by(message_id=message.id).first() is not None
        
        if old_exists and not new_exists:
            missing_in_new.append(message.id)
    
    if missing_in_new:
        print(f"   ⚠️  Mensajes con datos solo en estructura antigua: {missing_in_new}")
    else:
        print("   ✅ Todos los mensajes recientes tienen datos en ambas estructuras")
    print()
    
    # 3. Verificar categorías y subcategorías
    print("3. VERIFICACIÓN DE CATEGORÍAS:")
    categories = Category.query.all()
    print(f"   - Categorías disponibles: {len(categories)}")
    for cat in categories:
        subcat_count = Subcategory.query.filter_by(category_id=cat.id).count()
        values_count = ClassifiedValue.query.join(
            Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
        ).filter(Subcategory.category_id == cat.id).count()
        print(f"     * {cat.name}: {subcat_count} subcategorías, {values_count} valores")
    print()
    
    # 4. Verificar integridad de datos
    print("4. VERIFICACIÓN DE INTEGRIDAD:")
    
    # Verificar valores huérfanos
    orphaned_values = ClassifiedValue.query.outerjoin(
        Message, ClassifiedValue.message_id == Message.id
    ).filter(Message.id.is_(None)).count()
    
    orphaned_subcats = ClassifiedValue.query.outerjoin(
        Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
    ).filter(Subcategory.id.is_(None)).count()
    
    print(f"   - Valores sin mensaje asociado: {orphaned_values}")
    print(f"   - Valores sin subcategoría válida: {orphaned_subcats}")
    
    if orphaned_values == 0 and orphaned_subcats == 0:
        print("   ✅ Integridad de datos correcta")
    else:
        print("   ⚠️  Problemas de integridad detectados")
    print()
    
    # 5. Análisis de cobertura por categoría
    print("5. COBERTURA POR CATEGORÍA (estructura nueva):")
    
    category_coverage = {}
    for cat in categories:
        # Contar mensajes que deberían tener esta categoría según estructura antigua
        old_data_with_category = 0
        if cat.name == "Salud Física":
            old_data_with_category = ClassifiedData.query.filter(
                ClassifiedData.physical_health.isnot(None),
                ClassifiedData.physical_health != '[]'
            ).count()
        elif cat.name == "Salud Cognitiva":
            old_data_with_category = ClassifiedData.query.filter(
                ClassifiedData.cognitive_health.isnot(None),
                ClassifiedData.cognitive_health != '[]'
            ).count()
        elif cat.name == "Estado Emocional":
            old_data_with_category = ClassifiedData.query.filter(
                ClassifiedData.emotional_state.isnot(None),
                ClassifiedData.emotional_state != '[]'
            ).count()
        elif cat.name == "Medicación":
            old_data_with_category = ClassifiedData.query.filter(
                ClassifiedData.medication.isnot(None),
                ClassifiedData.medication != '[]'
            ).count()
        elif cat.name == "Gastos":
            old_data_with_category = ClassifiedData.query.filter(
                ClassifiedData.expenses.isnot(None),
                ClassifiedData.expenses != '[]'
            ).count()
        
        # Contar en estructura nueva
        new_data_with_category = ClassifiedValue.query.join(
            Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
        ).filter(Subcategory.category_id == cat.id).count()
        
        coverage_pct = (new_data_with_category / old_data_with_category * 100) if old_data_with_category > 0 else 100
        
        print(f"   - {cat.name}:")
        print(f"     * Estructura antigua: {old_data_with_category} registros")
        print(f"     * Estructura nueva: {new_data_with_category} valores")
        print(f"     * Cobertura: {coverage_pct:.1f}%")
        
        category_coverage[cat.name] = {
            'old': old_data_with_category,
            'new': new_data_with_category,
            'coverage': coverage_pct
        }
    print()
    
    # 6. Recomendaciones
    print("6. RECOMENDACIONES:")
    
    overall_health = True
    
    # Verificar si la migración está lista
    if new_count == 0:
        print("   ❌ La estructura nueva no tiene datos. Verificar que el guardado dual esté funcionando.")
        overall_health = False
    elif new_count < old_count * 0.8:
        print("   ⚠️  La estructura nueva tiene significativamente menos datos que la antigua.")
        print("      Revisar el proceso de guardado dual en classification_service.py")
        overall_health = False
    
    # Verificar cobertura por categorías
    low_coverage_categories = [cat for cat, data in category_coverage.items() if data['coverage'] < 80]
    if low_coverage_categories:
        print(f"   ⚠️  Categorías con baja cobertura: {', '.join(low_coverage_categories)}")
        print("      Revisar el mapeo de categorías en _save_normalized_classification")
        overall_health = False
    
    if overall_health:
        print("   ✅ SISTEMA LISTO PARA MIGRACIÓN")
        print("      Puedes proceder al Paso 2: Actualización de APIs")
    else:
        print("   ❌ PROBLEMAS DETECTADOS")
        print("      Resolver los problemas antes de continuar con la migración")
    
    print("\n=== FIN DE AUDITORÍA ===")
    
    return overall_health

if __name__ == "__main__":
    # Configurar para usar SQLite en desarrollo
    import os
    os.environ['FLASK_ENV'] = 'development'
    
    try:
        app = create_app()
        with app.app_context():
            audit_data_consistency()
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        print("\nPosibles soluciones:")
        print("1. Verificar que la base de datos SQLite existe en backend/instance/app.db")
        print("2. Verificar que las variables de entorno están configuradas correctamente")
        print("3. Ejecutar desde el directorio backend/")
        print("\nIntentando diagnóstico alternativo...")
        
        # Diagnóstico básico sin Flask app
        try:
            from sqlalchemy import create_engine, text
            import os
            
            # Intentar conectar directamente a SQLite
            db_path = os.path.join(os.getcwd(), 'instance', 'app.db')
            if os.path.exists(db_path):
                print(f"✅ Base de datos encontrada en: {db_path}")
                engine = create_engine(f'sqlite:///{db_path}')
                with engine.connect() as conn:
                    # Verificar tablas
                    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
                    tables = [row[0] for row in result]
                    print(f"✅ Tablas encontradas: {tables}")
                    
                    # Conteo básico si las tablas existen
                    if 'classified_data' in tables:
                        result = conn.execute(text("SELECT COUNT(*) FROM classified_data"))
                        old_count = result.scalar()
                        print(f"📊 Registros en classified_data: {old_count}")
                    
                    if 'classified_values' in tables:
                        result = conn.execute(text("SELECT COUNT(*) FROM classified_values"))
                        new_count = result.scalar()
                        print(f"📊 Registros en classified_values: {new_count}")
                    
                    if 'messages' in tables:
                        result = conn.execute(text("SELECT COUNT(*) FROM messages"))
                        msg_count = result.scalar()
                        print(f"📊 Registros en messages: {msg_count}")
            else:
                print(f"❌ Base de datos no encontrada en: {db_path}")
                print("Ejecutar: python create_db.py o python init_db.py")
                
        except Exception as e2:
            print(f"Error en diagnóstico alternativo: {e2}")