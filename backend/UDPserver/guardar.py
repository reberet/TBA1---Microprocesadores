import json
import os

ARCHIVO = "datos.json"

def validar_dato(dato):
    reglas = {
        "disco": (0, 100),
        "ilum": (0, 100),
        "puerta": (0, 1),
        "ruido": (0, 140),
        "temp": (0, 100),
        "fuego": (0, 1)
    }

    for clave in reglas.keys():
        if clave not in dato:
            return False, f"Falta la clave obligatoria: {clave}"

    for clave in dato.keys():
        if clave not in reglas:
            return False, f"Clave desconocida en JSON: {clave}"

    for clave, (min_val, max_val) in reglas.items():
        valor = dato[clave]
        if not isinstance(valor, (int, float)):
            return False, f"Valor inválido en {clave}: debe ser numérico"
        if not (min_val <= valor <= max_val):
            return False, f"{clave} fuera de rango ({valor}), esperado {min_val}-{max_val}"

    return True, "OK"


def guardar_datos(dato):
    valido, msg = validar_dato(dato)
    if not valido:
        print(f"❌ JSON rechazado: {msg}")
        return False, msg  # devolvemos False para que el server mande ERR

    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    with open(ARCHIVO, "r", encoding="utf-8") as f:
        try:
            datos = json.load(f)
            if not isinstance(datos, list):
                datos = []
        except json.JSONDecodeError:
            datos = []

    datos.append(dato)

    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print("✅ JSON válido guardado en datos.json")
    return True, "OK"
