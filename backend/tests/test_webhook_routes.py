#!/usr/bin/env python3
"""
Script para probar las rutas del webhook.
"""

import requests

def test_routes():
    """Prueba las rutas básicas de la API y webhook"""
    base_url = "http://localhost:5000"
    
    # Probar la ruta API de prueba
    print("\nProbando ruta API de prueba...")
    api_test_url = f"{base_url}/api/test"
    try:
        response = requests.get(api_test_url)
        print(f"Código de estado: {response.status_code}")
        print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Probar la ruta de prueba del webhook
    print("\nProbando ruta de prueba del webhook...")
    webhook_test_url = f"{base_url}/api/webhook/test"
    try:
        response = requests.get(webhook_test_url)
        print(f"Código de estado: {response.status_code}")
        print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Asegúrate de que la aplicación Flask esté en ejecución en http://localhost:5000")
    input("Presiona Enter para continuar con las pruebas...")
    test_routes()