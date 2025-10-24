import json
from pathlib import Path

# Ajustá la ruta según tu estructura
HISTORIAL_PATH = Path(__file__).parent.parent / "backend" / "data" / "historial.json"

def get_historial_reciente(limite=None):
    """
    Lee historial.json y devuelve los últimos eventos listos para mostrar en el frame.
    Cada registro del backend se transforma en un evento por cada campo de interés.
    """
    try:
        if not HISTORIAL_PATH.exists():
            print("⚠️ No se encontró el archivo historial.json.")
            return []

        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            historial = json.load(f)

        if not isinstance(historial, list):
            return []

        eventos_formateados = []
        campos = ["disco", "ilum", "puerta", "ruido", "temp", "fuego"]

        for registro in historial[-limite:]:
            for campo in campos:
                valor = registro.get(campo, -1)
                importancia = "Crítico" if valor == -1 else "Normal"
                eventos_formateados.append({
                    "dato": campo,
                    "valor_registrado": valor,
                    "importancia": importancia,
                    "hora": registro.get("hora", ""),
                    "mensaje": f"Valor registrado por {registro.get('emisor', '')}"
                })

        return eventos_formateados

    except Exception as e:
        print(f"❌ Error al leer historial.json: {e}")
        return []
    
def auto_refresh(self, intervalo_ms=5000):
        """Refresca la tabla automáticamente cada X milisegundos"""
        self.render_historial()
        self.after(intervalo_ms, self.auto_refresh)
