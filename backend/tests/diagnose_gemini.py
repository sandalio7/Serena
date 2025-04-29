import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
load_dotenv()

# Configurar API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: No se encontró la clave API de Google en las variables de entorno.")
    exit(1)

genai.configure(api_key=api_key)

def list_available_models():
    """Lista todos los modelos disponibles para la API key configurada"""
    try:
        print("Obteniendo lista de modelos disponibles...")
        models = genai.list_models()
        print(f"Se encontraron {len(list(models))} modelos disponibles:")
        
        for model in models:
            print(f"- ID: {model.name}")
            print(f"  Nombre para mostrar: {model.display_name}")
            print(f"  Descripción: {model.description}")
            print(f"  Generación: {model.generation_methods}")
            print("  ---")
            
    except Exception as e:
        print(f"Error al obtener modelos: {e}")
        
def test_model_connection(model_name):
    """Prueba la conexión al modelo especificado"""
    try:
        print(f"\nProbando conexión al modelo: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hola, ¿puedes responder a este mensaje de prueba?")
        print("Conexión exitosa. Respuesta de muestra:")
        print(response.text)
        return True
    except Exception as e:
        print(f"Error al conectar con el modelo {model_name}: {e}")
        return False

if __name__ == "__main__":
    # Listar modelos disponibles
    list_available_models()
    
    # Intentar conectar con los modelos más comunes
    test_models = [
        "gemini-pro", 
        "gemini-1.0-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "models/gemini-pro",
        "models/gemini-1.0-pro",
        "models/gemini-1.5-pro"
    ]
    
    successful_models = []
    for model in test_models:
        if test_model_connection(model):
            successful_models.append(model)
    
    print("\n--- RESUMEN ---")
    if successful_models:
        print(f"Modelos a los que se pudo conectar correctamente ({len(successful_models)}):")
        for model in successful_models:
            print(f"- {model}")
    else:
        print("No se pudo conectar a ninguno de los modelos probados.")
        print("Posibles soluciones:")
        print("1. Verificar que la API key sea válida y tenga los permisos adecuados")
        print("2. Revisar la documentación actual de Google para los nombres correctos de modelos")
        print("3. Comprobar si hay restricciones geográficas o de cuota en tu cuenta")