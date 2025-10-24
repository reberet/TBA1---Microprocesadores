"""
Gestor de Datos - Lee datos.json y los convierte a objetos Dato
"""
import json
from pathlib import Path
from typing import List
from models.dato import Dato, TipoDato, Alarma, EstadoBinario

class DatoManager:
    """Lee datos desde data/datos.json"""
    
    # Configuración de cada sensor (nombre, tipo, rango, etc)
    SENSOR_CONFIG = {
        "disco": {
            "nombre": "Disco Duro",
            "tipo": TipoDato.RANGO,
            "unidad": "%",
            "min": 0,
            "max": 90
        },
        "ilum": {
            "nombre": "Iluminación", 
            "tipo": TipoDato.RANGO,
            "unidad": "%",
            "min": 30,
            "max": 100
        },
        "puerta": {
            "nombre": "Puerta",
            "tipo": TipoDato.BINARIO
        },
        "ruido": {
            "nombre": "Nivel de Ruido",
            "tipo": TipoDato.RANGO,
            "unidad": "dB",
            "min": 0,
            "max": 70
        },
        "temp": {
            "nombre": "Temperatura",
            "tipo": TipoDato.RANGO,
            "unidad": "°C",
            "min": 18,
            "max": 28
        },
        "fuego": {
            "nombre": "Detector de Fuego",
            "tipo": TipoDato.BINARIO
        }
    }
    
    def __init__(self):
        self.datos_file = Path("backend/UDPserver/datos.json")
    
    def get_datos_activos(self) -> List[Dato]:
        """Lee datos.json y retorna lista de objetos Dato"""
        
        # Verificar que exista el archivo
        if not self.datos_file.exists():
            print(f"⚠️  No existe {self.datos_file}")
            return []
        
        # Leer JSON
        try:
            with open(self.datos_file, 'r') as f:
                raw_data = json.load(f)
            
            # Convertir a objetos Dato
            return self._json_to_datos(raw_data)
            
        except Exception as e:
            print(f"❌ Error leyendo datos: {e}")
            return []
    
    def _json_to_datos(self, raw_data: dict) -> List[Dato]:
        """Convierte JSON simple a objetos Dato"""
        datos = []
        
        for key, valor in raw_data.items():
            if key not in self.SENSOR_CONFIG:
                continue
            
            config = self.SENSOR_CONFIG[key]
            
            # Crear alarma según tipo
            if config["tipo"] == TipoDato.RANGO:
                alarma = Alarma(
                    tipo=TipoDato.RANGO,
                    valor_minimo=config["min"],
                    valor_maximo=config["max"]
                )
                valor_convertido = float(valor)
            else:  # BINARIO
                alarma = Alarma(
                    tipo=TipoDato.BINARIO,
                    estado_esperado=EstadoBinario.BIEN
                )
                valor_convertido = EstadoBinario.BIEN if valor == 0 else EstadoBinario.MAL
            
            # Crear Dato
            dato = Dato(
                nombre=config["nombre"],
                tipo=config["tipo"],
                valor=valor_convertido,
                unidad=config.get("unidad", ""),
                alarma=alarma,
                importancia="Normal"
            )
            
            datos.append(dato)
        
        return datos

# Instancia global
dato_manager = DatoManager()
