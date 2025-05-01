#!/usr/bin/env python3
"""
Script para probar el servicio GeminiService actualizado.
"""

import os
import sys
import json

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.gemini_service import GeminiService

def test_gemini_service():
    """Prueba el servicio de Gemini actualizado"""
    print("=== PRUEBA DEL SERVICIO GEMINI ===\n")
    
    # Inicializar el servicio
    try:
        print("1. Inicializando el servicio GeminiService...")
        gemini_service = GeminiService()
        print(f"✅ Servicio inicializado correctamente con el modelo: {gemini_service.model_name}")
    except Exception as e:
        print(f"❌ Error al inicializar el servicio: {e}")
        return
    
    # Probar conexión
    try:
        print("\n2. Probando conexión...")
        status, message = gemini_service.test_connection()
        if status:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return
    except Exception as e:
        print(f"❌ Error en la prueba de conexión: {e}")
        return
    
    # Probar clasificación
    print("\n3. Probando clasificación de mensajes...")
    test_messages = [
        "Hoy María estuvo un poco mejor. Caminó unos 100 pasos hasta el jardín y comió bien el almuerzo. Sigue olvidando tomar su medicamento para la presión, tuve que recordárselo tres veces. Gastamos 45€ en medicinas.",
        "José no pudo dormir bien anoche, estuvo inquieto. Solo tomó un vaso de leche en el desayuno y se negó a almorzar. Parece desorientado, preguntando varias veces qué día es hoy."
    ]
    
    for i, message in enumerate(test_messages):
        print(f"\n--- Mensaje de prueba {i+1} ---")
        print(message)
        try:
            result = gemini_service.classify_message(message)
            if "error" in result:
                print(f"❌ Error en la clasificación: {result['error']}")
            else:
                print("✅ Clasificación exitosa")
                # Mostrar categorías detectadas
                detected_categories = [cat["nombre"] for cat in result.get("categorias", []) if cat.get("detectada", False)]
                print(f"Categorías detectadas: {', '.join(detected_categories) if detected_categories else 'Ninguna'}")
                # Mostrar resumen
                print(f"Resumen: {result.get('resumen', 'No hay resumen')}")
                # Guardar resultado completo para inspección
                with open(f"classified_message_{i+1}.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                    print(f"Resultado guardado en classified_message_{i+1}.json")
        except Exception as e:
            print(f"❌ Error al procesar el mensaje: {e}")
    
    print("\n=== PRUEBA COMPLETADA ===")

if __name__ == "__main__":
    test_gemini_service()
    