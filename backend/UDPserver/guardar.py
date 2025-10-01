import json
import os
import datetime

VALIDADO = "datos.json"     # Este es el json de las validaciones (solo válidos)
HISTORIAL = "historial.json"  # Este es el historial (guarda todo con -1 si hay error)

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
        return False, msg

    if not os.path.exists(VALIDADO):
        with open(VALIDADO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    with open(VALIDADO, "r", encoding="utf-8") as f:
        try:
            datos = json.load(f)
            if not isinstance(datos, list):
                datos = []
        except json.JSONDecodeError:
            datos = []

    datos.append(dato)

    with open(VALIDADO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print("✅ JSON válido guardado en datos.json")
    return True, "OK"


def guardar_historial(dato):
    """
    Guarda SIEMPRE en historial.json.
    Si un valor es inválido, lo reemplaza por -1.
    Agrega hora y emisor.
    """
    reglas = {
        "disco": (0, 100),
        "ilum": (0, 100),
        "puerta": (0, 1),
        "ruido": (0, 140),
        "temp": (0, 100),
        "fuego": (0, 1)
    }

    # Copia para no modificar el original
    dato_hist = {}

    for clave, (min_val, max_val) in reglas.items():
        valor = dato.get(clave, -1)
        if isinstance(valor, (int, float)) and (min_val <= valor <= max_val):
            dato_hist[clave] = valor
        else:
            dato_hist[clave] = -1  # reemplazo por error

    # Agregar campos adicionales
    dato_hist["hora"] = datetime.datetime.now().isoformat(timespec="seconds")
    dato_hist["emisor"] = "SIM7000G"

    if not os.path.exists(HISTORIAL):
        with open(HISTORIAL, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    with open(HISTORIAL, "r", encoding="utf-8") as f:
        try:
            historial = json.load(f)
            if not isinstance(historial, list):
                historial = []
        except json.JSONDecodeError:
            historial = []

    historial.append(dato_hist)

    with open(HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

    print("📒 Historial actualizado en historial.json")
    return True, "OK"
