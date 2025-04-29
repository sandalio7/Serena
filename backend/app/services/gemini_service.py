import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument

# Configuración de logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Modelos disponibles (en orden de preferencia)
# Basado en las pruebas, el modelo lite ofrece el mejor balance entre rendimiento y costo
PRIMARY_MODEL = "models/gemini-2.0-flash-lite"
FALLBACK_MODELS = [
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro"
]

class GeminiService:
    """Servicio para interactuar con la API de Gemini AI"""
    
    def __init__(self):
        """Inicializa el servicio y configura el cliente de Gemini"""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.error("No se encontró la clave API de Google en las variables de entorno")
            raise ValueError("API key de Google no configurada")
        
        genai.configure(api_key=self.api_key)
        self.model_name = PRIMARY_MODEL
        self._verify_model_availability()
    
    def _verify_model_availability(self):
        """Verifica que el modelo preferido esté disponible"""
        try:
            logger.info(f"Verificando disponibilidad del modelo: {self.model_name}")
            model = genai.GenerativeModel(self.model_name)
            # Prueba una generación simple para verificar si el modelo funciona
            response = model.generate_content("Prueba de conexión", stream=False)
            if response:
                logger.info(f"Modelo verificado exitosamente: {self.model_name}")
                return True
        except Exception as e:
            logger.warning(f"No se pudo usar el modelo primario {self.model_name}: {str(e)}")
            # Intentar con modelos alternativos
            for alt_model in FALLBACK_MODELS:
                try:
                    logger.info(f"Probando modelo alternativo: {alt_model}")
                    model = genai.GenerativeModel(alt_model)
                    response = model.generate_content("Prueba de conexión", stream=False)
                    if response:
                        logger.info(f"Usando modelo alternativo: {alt_model}")
                        self.model_name = alt_model
                        return True
                except Exception as alt_e:
                    logger.warning(f"No se pudo usar el modelo alternativo {alt_model}: {str(alt_e)}")
                    continue
            
            logger.error("No se encontró ningún modelo disponible")
            raise RuntimeError("No se pudo conectar a ningún modelo de Gemini AI")
    
    def classify_message(self, message_text):
        """
        Clasifica un mensaje utilizando Gemini para extraer información estructurada.
        
        Args:
            message_text (str): El mensaje original del cuidador
            
        Returns:
            dict: Datos clasificados en categorías estructuradas
        """
        # Definir el prompt para clasificación
        prompt = self._create_classification_prompt(message_text)
        
        try:
            # Llamar a Gemini AI
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            # Procesar y limpiar la respuesta para obtener JSON válido
            return self._process_response(response)
            
        except Exception as e:
            logger.error(f"Error al clasificar mensaje: {str(e)}")
            # Intentar con modelos alternativos si falla el principal
            for alt_model in FALLBACK_MODELS:
                if alt_model != self.model_name:
                    try:
                        logger.info(f"Intentando clasificación con modelo alternativo: {alt_model}")
                        model = genai.GenerativeModel(alt_model)
                        response = model.generate_content(prompt)
                        result = self._process_response(response)
                        # Actualizar el modelo preferido si funciona bien
                        self.model_name = alt_model
                        logger.info(f"Clasificación exitosa con modelo alternativo: {alt_model}")
                        return result
                    except Exception as alt_e:
                        logger.warning(f"Error con modelo alternativo {alt_model}: {str(alt_e)}")
                        continue
            
            # Si ningún modelo funciona, devolver respuesta de error
            return {
                "categorias": [],
                "resumen": "Error en clasificación",
                "error": str(e)
            }
    
    def _create_classification_prompt(self, message_text):
        """Crea el prompt para la clasificación basado en el mensaje recibido"""
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
    
    def _process_response(self, response):
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
            logger.error(f"Error procesando respuesta: {e}")
            # Respuesta de fallback si hay error
            return {
                "categorias": [],
                "resumen": "Error en procesamiento de respuesta",
                "error": str(e)
            }
    
    def test_connection(self):
        """Prueba la conexión con el servicio de Gemini"""
        try:
            self._verify_model_availability()
            return True, f"Conexión exitosa con el modelo {self.model_name}"
        except Exception as e:
            return False, f"No se pudo establecer conexión: {str(e)}"