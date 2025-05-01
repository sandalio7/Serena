#!/usr/bin/env python3
"""
Script para probar las rutas de la aplicación.
"""

import requests
import sys

def test_routes():
    """Prueba las rutas básicas de la API"""
    base_url = "http://localhost:5000"
    
    # Definir las rutas a probar
    routes = [
        "/test",                    # Ruta de prueba básica
        "/api/health",              # Ruta de health check
        "/api/test",                # Ruta de test API
        "/api/webhook/test",        # Ruta de test del webhook
        "/api/webhook/whatsapp",    # Ruta del webhook de WhatsApp
    ]
    
    success = True
    
    print(f"{'=' * 50}")
    print("PROBANDO RUTAS DE LA APLICACIÓN")
    print(f"{'=' * 50}\n")
    
    for route in routes:
        url = f"{base_url}{route}"
        print(f"Probando ruta: {url}")
        try:
            response = requests.get(url)
            print(f"  Código de estado: {response.status_code}")
            print(f"  Contenido: {response.text}")
            if response.status_code == 404:
                print(f"  ❌ ERROR: Ruta no encontrada")
                success = False
            else:
                print(f"  ✅ ÉXITO: Ruta respondió correctamente")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            success = False
        print(f"{'-' * 50}")
    
    print(f"\n{'=' * 50}")
    if success:
        print("✅ TODAS LAS RUTAS FUNCIONAN CORRECTAMENTE")
    else:
        print("❌ ALGUNAS RUTAS NO FUNCIONAN CORRECTAMENTE")
    print(f"{'=' * 50}")
    
    return success

if __name__ == "__main__":
    print("Asegúrate de que la aplicación Flask esté en ejecución en http://localhost:5000")
    input("Presiona Enter para continuar con las pruebas...")
    success = test_routes()
    if not success:
        sys.exit(1)