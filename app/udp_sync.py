"""
UDP Sync - Sincroniza datos desde JSON UDP con el DatoManager
"""
import json
import threading
import time
from pathlib import Path
from models import dato_manager, TipoDato, EstadoBinario

class UDPSync:
    """Sincronizador de datos UDP con el sistema"""
    
    def __init__(self, json_path: str = "backend/UDPserver/datos.json", interval: float = 1.0):
        """
        Args:
            json_path: Ruta al archivo JSON con datos UDP
            interval: Intervalo de lectura en segundos
        """
        self.json_path = Path(__file__).parent / json_path
        self.interval = interval
        self.running = False
        self.thread = None
        self.last_data = {}
        
        # Mapeo de campos JSON a nombres de Datos
        self.field_mapping = {
            "disco": {
                "nombre": "Uso de Disco",
                "tipo": TipoDato.RANGO,
                "unidad": "%",
                "min": 0,
                "max": 90,
                "importancia": "Importante"
            },
            "ilum": {
                "nombre": "Iluminación",
                "tipo": TipoDato.RANGO,
                "unidad": "lux",
                "min": 0,
                "max": 100,
                "importancia": "Normal"
            },
            "puerta": {
                "nombre": "Estado Puerta",
                "tipo": TipoDato.BINARIO,
                "unidad": "",
                "min": 0,
                "max": 1,
                "importancia": "Crítico"
            },
            "ruido": {
                "nombre": "Nivel de Ruido",
                "tipo": TipoDato.RANGO,
                "unidad": "dB",
                "min": 0,
                "max": 80,
                "importancia": "Normal"
            },
            "temp": {
                "nombre": "Temperatura",
                "tipo": TipoDato.RANGO,
                "unidad": "°C",
                "min": 18,
                "max": 28,
                "importancia": "Crítico"
            },
            "fuego": {
                "nombre": "Detector de Fuego",
                "tipo": TipoDato.BINARIO,
                "unidad": "",
                "min": 0,
                "max": 1,
                "importancia": "Crítico"
            }
        }
    
    def start(self):
        """Inicia el thread de sincronización"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.thread.start()
        print("✅ UDP Sync iniciado")
    
    def stop(self):
        """Detiene el thread de sincronización"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        print("🛑 UDP Sync detenido")
    
    def _sync_loop(self):
        """Loop principal de sincronización"""
        while self.running:
            try:
                self._read_and_update()
            except Exception as e:
                print(f"❌ Error en sync: {e}")
            
            time.sleep(self.interval)
    
    def _read_and_update(self):
        """Lee el JSON y actualiza los datos"""
        if not self.json_path.exists():
            print(f"⚠️ Archivo no encontrado: {self.json_path}")
            return
        
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Si es un array, tomar el último elemento
            if isinstance(data, list):
                if not data:
                    return
                data = data[-1]
            
            # Si no hay cambios, no hacer nada
            if data == self.last_data:
                return
            
            self.last_data = data.copy()
            
            # Procesar cada campo del JSON
            for field, value in data.items():
                if field in self.field_mapping:
                    self._update_or_create_dato(field, value)
            
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"Error leyendo JSON: {e}")
    
    def _update_or_create_dato(self, field: str, value):
        """Actualiza o crea un dato basado en el campo JSON"""
        config = self.field_mapping[field]
        nombre = config["nombre"]
        
        # Buscar si ya existe el dato
        dato = dato_manager.buscar_dato(nombre)
        
        if dato:
            # Actualizar valor existente
            try:
                if config["tipo"] == TipoDato.RANGO:
                    dato_manager.actualizar_valor_dato(nombre, float(value))
                else:  # BINARIO
                    estado = EstadoBinario.BIEN if int(value) == 0 else EstadoBinario.MAL
                    dato_manager.actualizar_valor_dato(nombre, estado)
                
                print(f"📊 Actualizado: {nombre} = {value}")
            except Exception as e:
                print(f"Error actualizando {nombre}: {e}")
        else:
            # Crear nuevo dato
            try:
                if config["tipo"] == TipoDato.RANGO:
                    dato_manager.crear_dato_rango(
                        nombre=nombre,
                        valor_inicial=float(value),
                        unidad=config["unidad"],
                        valor_min=config["min"],
                        valor_max=config["max"],
                        importancia=config["importancia"]
                    )
                    print(f"✨ Creado nuevo dato RANGO: {nombre} = {value}")
                else:  # BINARIO
                    estado_inicial = EstadoBinario.BIEN if int(value) == 0 else EstadoBinario.MAL
                    estado_esperado = EstadoBinario.BIEN  # 0 = cerrado/sin fuego = BIEN
                    dato_manager.crear_dato_binario(
                        nombre=nombre,
                        valor_inicial=estado_inicial,
                        estado_esperado=estado_esperado,
                        importancia=config["importancia"]
                    )
                    print(f"✨ Creado nuevo dato BINARIO: {nombre} = {estado_inicial.value}")
            except Exception as e:
                print(f"Error creando {nombre}: {e}")
    
    def add_field_mapping(self, field: str, nombre: str, tipo: TipoDato, 
                          unidad: str = "", min_val: float = 0, max_val: float = 100,
                          importancia: str = "Normal"):
        """
        Agrega un nuevo mapeo de campo JSON a Dato
        
        Args:
            field: Nombre del campo en el JSON (ej: "humidity")
            nombre: Nombre del Dato en el sistema (ej: "Humedad")
            tipo: TipoDato.RANGO o TipoDato.BINARIO
            unidad: Unidad de medida (ej: "%")
            min_val: Valor mínimo para alarma
            max_val: Valor máximo para alarma
            importancia: Normal, Importante, Crítico
        """
        self.field_mapping[field] = {
            "nombre": nombre,
            "tipo": tipo,
            "unidad": unidad,
            "min": min_val,
            "max": max_val,
            "importancia": importancia
        }
        print(f"➕ Mapeo agregado: {field} → {nombre}")

# Instancia global
udp_sync = UDPSync()
