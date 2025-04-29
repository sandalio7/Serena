#!/usr/bin/env python3
"""
Script para probar la disponibilidad y funcionamiento de los modelos de Gemini.
"""

import os
import sys

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

def test_gemini_models():
    """Prueba los modelos específicos de Gemini"""
    models_to_test = [
        "2.0-flash-lite",
        "2.5-flash",
        "2.5-pro"
    ]
    
    print("=== PRUEBA DE MODELOS GEMINI ===\n")
    
    # Listar modelos disponibles
    try:
        print("Obteniendo lista de modelos disponibles...")
        models = genai.list_models()
        available_models = list(models)
        
        print(f"Se encontraron {len(available_models)} modelos disponibles:")
        for model in available_models:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error al obtener la lista de modelos: {e}")
    
    # Probar los modelos específicos
    print("\n--- Probando modelos específicos ---")
    
    for model_name in models_to_test:
        try:
            print(f"\nProbando modelo: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Prueba de conexión: ¿Puedes responder a este mensaje?")
            print("✅ Conexión exitosa")
            print(f"Respuesta: {response.text}")
        except Exception as e:
            print(f"❌ Error al conectar con el modelo {model_name}: {e}")

if __name__ == "__main__":
    test_gemini_models()