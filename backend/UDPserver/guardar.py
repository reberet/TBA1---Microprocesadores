import json
import os

ARCHIVO = "datos.json"

def guardar_datos(dato):
    try:
        # Validar que sea JSON serializable
        json_str = json.dumps(dato)  
        obj = json.loads(json_str)   # vuelve a cargarlo para asegurar
    except (TypeError, json.JSONDecodeError):
        print("❌ El dato recibido NO es un JSON válido. Se descarta.")
        return  # no se guarda nada

    # Si no existe el archivo, lo creamos con una lista vacía
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    # Leemos el contenido actual
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        try:
            datos = json.load(f)
            if not isinstance(datos, list):
                datos = []
        except json.JSONDecodeError:
            datos = []

    # Agregamos el nuevo objeto
    datos.append(obj)

    # Sobrescribimos el archivo con todo el historial
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print("✅ JSON válido guardado en datos.json")

