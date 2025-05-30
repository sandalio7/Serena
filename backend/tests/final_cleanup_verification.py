# backend/tests/final_cleanup_verification.py
"""
Script para limpieza final y verificación completa de la migración
"""

import os
import sys
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def scan_for_classified_data_references():
    """
    Escanea todos los archivos Python en busca de referencias a classified_data
    """
    print("=== ESCANEANDO REFERENCIAS A classified_data ===\n")
    
    # Directorios a escanear
    directories_to_scan = [
        'app',
        'tests'
    ]
    
    # Patrones a buscar
    patterns = [
        r'from.*classified_data',
        r'import.*classified_data',
        r'ClassifiedData',
        r'classified_data\.',
        r'\.classified_data',
    ]
    
    found_references = []
    
    for directory in directories_to_scan:
        if not os.path.exists(directory):
            continue
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.split('\n')
                            
                            for line_num, line in enumerate(lines, 1):
                                for pattern in patterns:
                                    if re.search(pattern, line, re.IGNORECASE):
                                        found_references.append({
                                            'file': file_path,
                                            'line': line_num,
                                            'content': line.strip(),
                                            'pattern': pattern
                                        })
                    except Exception as e:
                        print(f"Error leyendo {file_path}: {e}")
    
    if found_references:
        print("❌ REFERENCIAS A classified_data ENCONTRADAS:")
        for ref in found_references:
            print(f"   📁 {ref['file']}:{ref['line']}")
            print(f"   📝 {ref['content']}")
            print(f"   🔍 Patrón: {ref['pattern']}\n")
        
        return False
    else:
        print("✅ No se encontraron referencias a classified_data")
        return True

def check_import_errors():
    """
    Verifica que no hay errores de importación en los módulos principales
    """
    print("\n=== VERIFICANDO IMPORTS ===\n")
    
    modules_to_test = [
        'app.services.classification_service',
        'app.api.health_data', 
        'app.api.financial_data',
        'app.models.classified_value',
        'app.models.category',
        'app.models.subcategory',
        'app.models.message',
        'app.models.patient',
        'app.models.caregiver'
    ]
    
    all_imports_ok = True
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            all_imports_ok = False
        except Exception as e:
            print(f"⚠️  {module_name}: {e}")
            all_imports_ok = False
    
    return all_imports_ok

def test_database_structure():
    """
    Verifica que la estructura de base de datos es correcta
    """
    print("\n=== VERIFICANDO ESTRUCTURA DE BASE DE DATOS ===\n")
    
    try:
        from app import create_app
        from app.extensions import db
        from app.models.classified_value import ClassifiedValue
        from app.models.category import Category
        from app.models.subcategory import Subcategory
        from app.models.message import Message
        from sqlalchemy import inspect
        
        app = create_app()
        with app.app_context():
            # Verificar conexión
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # Tablas que DEBEN existir
            required_tables = [
                'classified_values',
                'categories', 
                'subcategories',
                'messages',
                'patients',
                'caregivers'
            ]
            
            # Tablas que NO deben existir
            forbidden_tables = [
                'classified_data'
            ]
            
            print("Verificando tablas requeridas:")
            all_required_present = True
            for table in required_tables:
                if table in existing_tables:
                    print(f"✅ {table}")
                else:
                    print(f"❌ {table} - FALTANTE")
                    all_required_present = False
            
            print("\nVerificando tablas prohibidas:")
            no_forbidden_present = True
            for table in forbidden_tables:
                if table in existing_tables:
                    print(f"❌ {table} - DEBE SER ELIMINADA")
                    no_forbidden_present = False
                else:
                    print(f"✅ {table} - Correctamente eliminada")
            
            # Verificar que podemos hacer queries básicas
            print("\nVerificando queries básicas:")
            try:
                categories_count = Category.query.count()
                subcategories_count = Subcategory.query.count()
                values_count = ClassifiedValue.query.count()
                messages_count = Message.query.count()
                
                print(f"✅ Categories: {categories_count}")
                print(f"✅ Subcategories: {subcategories_count}")
                print(f"✅ Classified Values: {values_count}")
                print(f"✅ Messages: {messages_count}")
                
                queries_ok = True
            except Exception as e:
                print(f"❌ Error en queries: {e}")
                queries_ok = False
            
            return all_required_present and no_forbidden_present and queries_ok
            
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

def test_classification_service():
    """
    Prueba básica del servicio de clasificación
    """
    print("\n=== PROBANDO SERVICIO DE CLASIFICACIÓN ===\n")
    
    try:
        from app.services.classification_service import ClassificationService
        
        # Crear instancia del servicio
        service = ClassificationService()
        print("✅ ClassificationService instanciado correctamente")
        
        # Verificar que tiene los métodos necesarios
        required_methods = [
            'process_message',
            '_save_normalized_classification',
            'get_patient_classification_summary'
        ]
        
        methods_ok = True
        for method_name in required_methods:
            if hasattr(service, method_name):
                print(f"✅ Método {method_name} presente")
            else:
                print(f"❌ Método {method_name} faltante")
                methods_ok = False
        
        return methods_ok
        
    except Exception as e:
        print(f"❌ Error probando ClassificationService: {e}")
        return False

def main():
    """
    Función principal de verificación
    """
    print("MIGRACIÓN LIMPIA - VERIFICACIÓN FINAL")
    print("="*60)
    
    # Paso 1: Escanear referencias
    step1_ok = scan_for_classified_data_references()
    
    # Paso 2: Verificar imports
    step2_ok = check_import_errors()
    
    # Paso 3: Verificar base de datos
    step3_ok = test_database_structure()
    
    # Paso 4: Probar servicio de clasificación
    step4_ok = test_classification_service()
    
    # Resultado final
    print("\n" + "="*60)
    print("RESULTADO FINAL DE LA MIGRACIÓN:")
    
    if step1_ok and step2_ok and step3_ok and step4_ok:
        print("🎉 ✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("\nLa migración limpia de classified_data a classified_values ha sido completada.")
        print("El sistema ahora usa exclusivamente la estructura normalizada.")
        print("\nPuedes continuar con el desarrollo normal del proyecto.")
        
        print("\n📋 RESUMEN DE CAMBIOS:")
        print("✅ Tabla classified_data eliminada")
        print("✅ Modelo ClassifiedData eliminado")
        print("✅ ClassificationService actualizado")
        print("✅ APIs health_data.py y financial_data.py actualizadas")
        print("✅ Solo se usa la estructura normalizada (classified_values)")
        
        return True
    else:
        print("❌ MIGRACIÓN INCOMPLETA - REVISAR ERRORES")
        print("\nSe encontraron problemas que deben resolverse:")
        
        if not step1_ok:
            print("❌ Referencias a classified_data aún presentes")
        if not step2_ok:
            print("❌ Errores de importación")
        if not step3_ok:
            print("❌ Problemas en estructura de base de datos")
        if not step4_ok:
            print("❌ Problemas en servicio de clasificación")
            
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)