import json
import os

# Obtener la ruta del directorio actual (donde está guardar.py)
DIRECTORIO = os.path.dirname(__file__)
ARCHIVO = os.path.join(DIRECTORIO, "datos.json")

def guardar_datos(dato):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(dato, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Datos guardados en {ARCHIVO}")
