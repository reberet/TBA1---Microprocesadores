import json

def guardar_datos(dato):
    with open("../datos.json", "w") as archivo:
        json.dump(dato, archivo, indent=4)


