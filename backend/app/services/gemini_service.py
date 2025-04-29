# backend/app/services/gemini_service.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno para asegurarnos de tener la API key
load_dotenv()

# Configurar la API key de Google
api_key = os.environ.get('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("No se encontró la API key de Google. Asegúrate de configurar GOOGLE_API_KEY en .env")

genai.configure(api_key=api_key)

def classify_message(message_text):
    """
    Clasifica un mensaje utilizando Gemini AI para extraer información estructurada.
    
    Args:
        message_text (str): El mensaje original del cuidador
        
    Returns:
        dict: Datos clasificados en categorías estructuradas
    """
    # Definir el prompt para clasificación
    prompt = f"""
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
    
    try:
        # Llamar a Gemini AI
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Procesar y limpiar la respuesta para obtener JSON válido
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
            "resumen": "Error en clasificación",
            "error": str(e)
        }

# Función para extraer datos específicos por categoría
def extract_data_by_category(classified_data, category_name):
    """
    Extrae datos específicos de una categoría del resultado de clasificación
    
    Args:
        classified_data (dict): Datos clasificados
        category_name (str): Nombre de la categoría a extraer
        
    Returns:
        dict: Datos de la categoría solicitada
    """
    for category in classified_data.get('categorias', []):
        if category['nombre'] == category_name and category.get('detectada', False):
            return {
                'detectada': True,
                'subcategorias': category.get('subcategorias', [])
            }
    
    return {'detectada': False, 'subcategorias': []}