#!/usr/bin/env python
"""Script de pruebas para la API de Monitoreo de CO2."""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Prueba el estado de la API."""
    print("\n🔍 Probando estado de la API...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_generar_datos():
    """Genera datos de prueba."""
    print("\n📊 Generando datos de prueba...")
    response = requests.post(f"{BASE_URL}/generar-datos?cantidad=500")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_crear_lectura():
    """Crea una nueva lectura."""
    print("\n📝 Creando lectura...")
    data = {
        "co2_ppm": 950.5,
        "temperatura": 23.2,
        "laboratorio": "Lab-Sw-01"
    }
    response = requests.post(f"{BASE_URL}/lecturas", json=data)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_obtener_lecturas():
    """Obtiene historial de lecturas."""
    print("\n📋 Obteniendo historial de lecturas...")
    response = requests.get(f"{BASE_URL}/lecturas?limite=5")
    print(f"Status: {response.status_code}")
    print(f"Total registros: {len(response.json())}")
    if response.json():
        print(f"Primera lectura: {json.dumps(response.json()[0], indent=2)}")
    return response.status_code == 200

def test_ultima_lectura():
    """Obtiene la última lectura."""
    print("\n⏰ Obteniendo última lectura...")
    response = requests.get(f"{BASE_URL}/lecturas/ultima")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_estadisticas():
    """Obtiene estadísticas."""
    print("\n📈 Obteniendo estadísticas...")
    response = requests.get(f"{BASE_URL}/lecturas/estadisticas")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_reporte():
    """Obtiene reporte por rango de fechas."""
    print("\n📅 Obteniendo reporte por fechas...")
    response = requests.get(f"{BASE_URL}/lecturas/reporte?fecha_inicio=2025-01-01&fecha_fin=2026-12-31")
    print(f"Status: {response.status_code}")
    print(f"Total registros en rango: {len(response.json())}")
    return response.status_code == 200

def test_clustering():
    """Ejecuta análisis de clustering."""
    print("\n🔬 Ejecutando análisis de clustering...")
    response = requests.post(f"{BASE_URL}/clustering/analizar")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, default=str)}")
    return response.status_code == 200

def test_eliminar_lectura():
    """Elimina una lectura."""
    print("\n🗑️  Eliminando lectura...")
    response = requests.delete(f"{BASE_URL}/lecturas/1")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("=" * 60)
    print("🧪 PRUEBAS DE API - SISTEMA DE MONITOREO DE CO2")
    print("=" * 60)

    tests = [
        ("Health Check", test_health),
        ("Generar Datos", test_generar_datos),
        ("Crear Lectura", test_crear_lectura),
        ("Obtener Lecturas", test_obtener_lecturas),
        ("Última Lectura", test_ultima_lectura),
        ("Estadísticas", test_estadisticas),
        ("Reporte", test_reporte),
        ("Clustering", test_clustering),
    ]

    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results[name] = False

    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    for name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {name}")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\nTotal: {passed}/{total} pruebas exitosas")

if __name__ == "__main__":
    run_all_tests()
