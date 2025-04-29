#!/usr/bin/env python3
"""
Script para probar y comparar la precisión de clasificación entre los modelos de Gemini.
"""

import os
import sys
import json
import time

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: No se encontró la clave API de Google en las variables de entorno.")
    exit(1)

genai.configure(api_key=api_key)

def create_classification_prompt(message_text):
    """Crea el prompt para la clasificación"""
    return f"""
    Actúa como un sistema de clasificación de mensajes para cuidadores de personas mayores o con condiciones neurodegenerativas.
    
    Analiza el siguiente mensaje y extrae información estructurada según estas categorías:
    
    1. Salud Física:
       - Movilidad (pasos, distancia)
       - Alimentación (comidas, apetito)
       - Sueño (horas, calidad)
       - Síntomas (dolor, malestar)
    
    2. Salud Cognitiva:
       - Memoria (olvidos, reconocimiento)
       - Orientación (tiempo, lugar)
       - Comunicación (claridad, coherencia)
    
    3. Estado Emocional:
       - Humor (alegría, tristeza, irritabilidad)
       - Sociabilidad (interacción, aislamiento)
       - Agitación (inquietud, ansiedad)
    
    4. Medicación:
       - Adherencia (toma, rechazo)
       - Efectos (reacciones, eficacia)
    
    5. Gastos:
       - Medicamentos (costos)
       - Servicios (costos)
       - Otros (detallar)
    
    Mensaje del cuidador:
    "{message_text}"
    
    Devuelve SOLO un objeto JSON con esta estructura, sin explicaciones adicionales:
    {{
        "categorias": [
            {{
                "nombre": "Salud Física",
                "detectada": true/false,
                "subcategorias": [
                    {{
                        "nombre": "Movilidad",
                        "detectada": true/false,
                        "valor": "texto extraído",
                        "confianza": 0.9 // número entre 0 y 1
                    }},
                    // Otras subcategorías...
                ]
            }},
            // Otras categorías...
        ],
        "resumen": "Breve resumen del estado general del paciente basado en el mensaje"
    }}
    """

def process_response(response):
    """Procesa la respuesta del modelo para extraer el JSON válido"""
    try:
        response_text = response.text
        # Si la respuesta contiene bloques de código, extraer solo el JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        # Convertir respuesta a diccionario
        classified_data = json.loads(response_text)
        return classified_data
        
    except Exception as e:
        print(f"Error procesando respuesta: {e}")
        # Respuesta de fallback si hay error
        return {
            "categorias": [],
            "resumen": "Error en procesamiento de respuesta",
            "error": str(e)
        }

def evaluate_classification(result):
    """Evalúa la calidad de la clasificación"""
    # Contar categorías detectadas
    detected_categories = 0
    detected_subcategories = 0
    
    for category in result.get("categorias", []):
        if category.get("detectada", False):
            detected_categories += 1
            for subcategory in category.get("subcategorias", []):
                if subcategory.get("detectada", False):
                    detected_subcategories += 1
    
    # Verificar si hay un resumen
    has_summary = bool(result.get("resumen", "").strip())
    
    # Verificar si hay valores en las subcategorías
    has_values = False
    for category in result.get("categorias", []):
        for subcategory in category.get("subcategorias", []):
            if subcategory.get("detectada", False) and subcategory.get("valor", "").strip():
                has_values = True
                break
    
    return {
        "detected_categories": detected_categories,
        "detected_subcategories": detected_subcategories,
        "has_summary": has_summary,
        "has_values": has_values
    }

def test_model_classification(model_name, test_messages):
    """Prueba la clasificación con un modelo específico"""
    print(f"\n=== PRUEBA DE CLASIFICACIÓN CON MODELO: {model_name} ===\n")
    
    results = []
    total_time = 0
    success_count = 0
    
    try:
        model = genai.GenerativeModel(model_name)
        
        for i, message in enumerate(test_messages):
            print(f"\nMensaje de prueba {i+1}:")
            print(message)
            
            try:
                # Medir tiempo
                start_time = time.time()
                
                # Clasificar mensaje
                prompt = create_classification_prompt(message)
                response = model.generate_content(prompt)
                result = process_response(response)
                
                # Calcular tiempo
                end_time = time.time()
                elapsed_time = end_time - start_time
                total_time += elapsed_time
                
                # Evaluar clasificación
                evaluation = evaluate_classification(result)
                
                print(f"✅ Clasificación exitosa en {elapsed_time:.2f} segundos")
                print(f"Categorías detectadas: {evaluation['detected_categories']}")
                print(f"Subcategorías detectadas: {evaluation['detected_subcategories']}")
                
                results.append({
                    "message_index": i,
                    "time": elapsed_time,
                    "evaluation": evaluation,
                    "result": result
                })
                
                success_count += 1
                
            except Exception as e:
                print(f"❌ Error en la clasificación: {e}")
                results.append({
                    "message_index": i,
                    "error": str(e)
                })
        
        # Mostrar resumen
        if success_count > 0:
            avg_time = total_time / success_count
            print(f"\n--- RESUMEN DE CLASIFICACIÓN CON {model_name} ---")
            print(f"Tiempo promedio: {avg_time:.2f} segundos")
            print(f"Tasa de éxito: {success_count}/{len(test_messages)}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error al inicializar el modelo {model_name}: {e}")
        return []

def compare_models():
    """Compara la clasificación entre diferentes modelos"""
    # Mensajes de prueba
    test_messages = [
        "Hoy María estuvo un poco mejor. Caminó unos 100 pasos hasta el jardín y comió bien el almuerzo. Sigue olvidando tomar su medicamento para la presión, tuve que recordárselo tres veces. Gastamos 45€ en medicinas.",
        "José no pudo dormir bien anoche, estuvo inquieto. Solo tomó un vaso de leche en el desayuno y se negó a almorzar. Parece desorientado, preguntando varias veces qué día es hoy.",
        "Carmen está más animada hoy. Habló por teléfono con su hija y eso le alegró mucho. Caminamos al parque (unos 200 metros) y se sentó un rato al sol. Tomó toda su medicación sin problemas. El fisioterapeuta cobró 60€ por la sesión de hoy."
    ]
    
    # Modelos a comparar (usando nombres correctos de la lista)
    models_to_test = [
        "models/gemini-2.0-flash-lite",
        "models/gemini-2.0-flash"
    ]
    
    all_results = {}
    
    for model_name in models_to_test:
        all_results[model_name] = test_model_classification(model_name, test_messages)
    
    # Comparación final
    print("\n=== COMPARACIÓN FINAL DE MODELOS ===")
    for model_name, results in all_results.items():
        successful_tests = [r for r in results if "error" not in r]
        if successful_tests:
            avg_time = sum(r["time"] for r in successful_tests) / len(successful_tests)
            avg_categories = sum(r["evaluation"]["detected_categories"] for r in successful_tests) / len(successful_tests)
            avg_subcategories = sum(r["evaluation"]["detected_subcategories"] for r in successful_tests) / len(successful_tests)
            
            print(f"\nModelo: {model_name}")
            print(f"Tiempo promedio: {avg_time:.2f} segundos")
            print(f"Promedio de categorías detectadas: {avg_categories:.1f}")
            print(f"Promedio de subcategorías detectadas: {avg_subcategories:.1f}")
            print(f"Tasa de éxito: {len(successful_tests)}/{len(results)}")
        else:
            print(f"\nModelo: {model_name}")
            print("No se completaron pruebas exitosamente")

if __name__ == "__main__":
    compare_models()