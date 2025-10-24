"""
Modelos de datos - Define las estructuras de datos y alarmas
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Union
from datetime import datetime

class TipoDato(Enum):
    """Tipos de datos que se pueden monitorear"""
    RANGO = "rango"  # Datos con valor numérico en un rango (ej: temperatura 25-40°C)
    BINARIO = "binario"  # Datos de dos estados (ej: puerta abierta/cerrada)

class EstadoBinario(Enum):
    """Estados para datos binarios"""
    BIEN = "bien"
    MAL = "mal"

@dataclass
class Alarma:
    """Configuración de alarma para un dato"""
    tipo: TipoDato
    # Para tipo RANGO
    valor_minimo: Optional[float] = None
    valor_maximo: Optional[float] = None
    # Para tipo BINARIO
    estado_esperado: Optional[EstadoBinario] = None
    
    def validar(self, valor: Union[float, str, EstadoBinario]) -> tuple[bool, str]:
        """
        Valida si un valor está dentro de los parámetros de la alarma
        
        Returns:
            tuple: (es_valido, mensaje)
        """
        if self.tipo == TipoDato.RANGO:
            try:
                valor_num = float(valor)
                if self.valor_minimo is not None and valor_num < self.valor_minimo:
                    return False, f"Valor {valor_num} por debajo del mínimo {self.valor_minimo}"
                if self.valor_maximo is not None and valor_num > self.valor_maximo:
                    return False, f"Valor {valor_num} por encima del máximo {self.valor_maximo}"
                return True, "Valor dentro del rango"
            except (ValueError, TypeError):
                return False, "Valor no numérico"
        
        elif self.tipo == TipoDato.BINARIO:
            if isinstance(valor, str):
                valor = EstadoBinario.BIEN if valor.lower() in ['bien', 'ok', 'true'] else EstadoBinario.MAL
            
            if valor != self.estado_esperado:
                return False, f"Estado {valor.value} no es el esperado ({self.estado_esperado.value})"
            return True, "Estado correcto"
        
        return False, "Tipo de dato desconocido"

@dataclass
class Dato:
    """Representa un dato a monitorear en el sistema"""
    nombre: str
    tipo: TipoDato
    valor: Union[float, str, EstadoBinario]
    unidad: str = ""  # Ej: "°C", "%", "bar"
    alarma: Optional[Alarma] = None
    importancia: str = "Normal"  # Normal, Importante, Crítico
    activo: bool = True
    ultima_actualizacion: datetime = field(default_factory=datetime.now)
    
    def actualizar_valor(self, nuevo_valor: Union[float, str, EstadoBinario]):
        """Actualiza el valor del dato"""
        self.valor = nuevo_valor
        self.ultima_actualizacion = datetime.now()
    
    def esta_en_alarma(self) -> tuple[bool, str]:
        """
        Verifica si el dato actual está en estado de alarma
        
        Returns:
            tuple: (en_alarma, mensaje)
        """
        if not self.alarma:
            return False, "Sin alarma configurada"
        
        es_valido, mensaje = self.alarma.validar(self.valor)
        return not es_valido, mensaje
    
    def get_valor_formateado(self) -> str:
        """Retorna el valor formateado con su unidad"""
        if self.tipo == TipoDato.BINARIO:
            if isinstance(self.valor, EstadoBinario):
                return self.valor.value.capitalize()
            return str(self.valor)
        else:
            return f"{self.valor}{self.unidad}"
    
    def to_dict(self) -> dict:
        """Convierte el dato a diccionario para serialización"""
        return {
            'nombre': self.nombre,
            'tipo': self.tipo.value,
            'valor': self.valor if not isinstance(self.valor, EstadoBinario) else self.valor.value,
            'unidad': self.unidad,
            'importancia': self.importancia,
            'activo': self.activo,
            'ultima_actualizacion': self.ultima_actualizacion.isoformat(),
            'alarma': {
                'tipo': self.alarma.tipo.value,
                'valor_minimo': self.alarma.valor_minimo,
                'valor_maximo': self.alarma.valor_maximo,
                'estado_esperado': self.alarma.estado_esperado.value if self.alarma.estado_esperado else None
            } if self.alarma else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Dato':
        """Crea un Dato desde un diccionario"""
        tipo = TipoDato(data['tipo'])
        
        # Reconstruir alarma si existe
        alarma = None
        if data.get('alarma'):
            alarma_data = data['alarma']
            alarma = Alarma(
                tipo=TipoDato(alarma_data['tipo']),
                valor_minimo=alarma_data.get('valor_minimo'),
                valor_maximo=alarma_data.get('valor_maximo'),
                estado_esperado=EstadoBinario(alarma_data['estado_esperado']) if alarma_data.get('estado_esperado') else None
            )
        
        # Convertir valor según tipo
        valor = data['valor']
        if tipo == TipoDato.BINARIO and isinstance(valor, str):
            valor = EstadoBinario(valor)
        
        return cls(
            nombre=data['nombre'],
            tipo=tipo,
            valor=valor,
            unidad=data.get('unidad', ''),
            alarma=alarma,
            importancia=data.get('importancia', 'Normal'),
            activo=data.get('activo', True),
            ultima_actualizacion=datetime.fromisoformat(data['ultima_actualizacion'])
        )

# Ejemplos de uso
def crear_dato_temperatura() -> Dato:
    """Ejemplo: Crear dato de temperatura con alarma de rango"""
    alarma = Alarma(
        tipo=TipoDato.RANGO,
        valor_minimo=25.0,
        valor_maximo=40.0
    )
    return Dato(
        nombre="Temperatura",
        tipo=TipoDato.RANGO,
        valor=38.0,
        unidad="°C",
        alarma=alarma,
        importancia="Importante"
    )

def crear_dato_puerta() -> Dato:
    """Ejemplo: Crear dato binario de estado de puerta"""
    alarma = Alarma(
        tipo=TipoDato.BINARIO,
        estado_esperado=EstadoBinario.BIEN
    )
    return Dato(
        nombre="Puerta Principal",
        tipo=TipoDato.BINARIO,
        valor=EstadoBinario.BIEN,
        alarma=alarma,
        importancia="Crítico"
    )
