# backend/tests/test_gemini_integration.py
import os
import sys
import pytest
from pathlib import Path

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.gemini_service import classify_message

@pytest.mark.integration
def test_gemini_classification():
    """Prueba de integración con Gemini AI"""
    # Mensaje de prueba
    test_message = "Hoy María estuvo un poco mejor. Caminó unos 100 pasos hasta el jardín y comió bien el almuerzo. Sigue olvidando tomar su medicamento para la presión, tuve que recordárselo tres veces. Gastamos 45€ en medicinas."
    
    print("\n--- Mensaje de prueba ---")
    print(test_message)
    
    # Clasificar mensaje
    result = classify_message(test_message)
    
    print("\n--- Resultado de clasificación ---")
    print(result)
    
    # Verificar si hay resumen
    if 'resumen' in result:
        print("\n--- Resumen generado ---")
        print(result['resumen'])
    
    # Verificaciones básicas
    assert result is not None
    assert "categorias" in result
    assert "resumen" in result
    
    return result

if __name__ == "__main__":
    # Ejecutar la prueba directamente si se llama como script
    test_gemini_classification()