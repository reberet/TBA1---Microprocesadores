"""
Widget Component - Componente visual dinámico para mostrar datos
"""
from tkinter import Canvas
from models.dato import Dato, TipoDato, EstadoBinario

class Widget:
    """Componente visual que se genera dinámicamente basado en un Dato"""
    
    def __init__(self, canvas: Canvas, dato: Dato, x: float, y: float, 
                 width: float = 305.0, height: float = 290.0):
        """
        Inicializa un widget
        
        Args:
            canvas: Canvas donde se dibujará
            dato: Objeto Dato que representa este widget
            x, y: Posición superior izquierda
            width, height: Dimensiones del widget
        """
        self.canvas = canvas
        self.dato = dato
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.elements = []  # Para guardar referencias
        
    def render(self):
        """Renderiza el widget según el tipo de dato"""
        if self.dato.tipo == TipoDato.RANGO:
            self._render_rango()
        elif self.dato.tipo == TipoDato.BINARIO:
            self._render_binario()
    
    def _render_rango(self):
        """Renderiza widget para dato de tipo RANGO"""
        # Determinar color según si está en alarma
        en_alarma, mensaje = self.dato.esta_en_alarma()
        color_barra = "#F8BC04" if not en_alarma else "#FF4444"  # Amarillo o Rojo
        color_fondo = "#0E1D3A"
        
        # Fondo del widget
        rect_fondo = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill=color_fondo,
            outline=""
        )
        self.elements.append(rect_fondo)
        
        # Barra inferior con color de estado
        barra_height = 36.0
        rect_barra = self.canvas.create_rectangle(
            self.x, self.y + self.height - barra_height,
            self.x + self.width, self.y + self.height,
            fill=color_barra,
            outline=""
        )
        self.elements.append(rect_barra)
        
        # Label del nombre del dato
        text_nombre = self.canvas.create_text(
            self.x + 21.0,
            self.y + self.height - barra_height + 4.0,
            anchor="nw",
            text=self.dato.nombre,
            fill="#FFFFFF",
            font=("ArialMT", 16)
        )
        self.elements.append(text_nombre)
        
        # Valor principal (grande)
        valor_texto = f"{self.dato.valor:.0f}°" if self.dato.unidad == "°C" else f"{self.dato.valor:.1f}"
        text_valor = self.canvas.create_text(
            self.x + 80.0,
            self.y + 94.0,
            anchor="nw",
            text=valor_texto,
            fill="#FFFFFF",
            font=("ArialMT", 48)
        )
        self.elements.append(text_valor)
        
        # Unidad (si no es °C que ya se incluye arriba)
        if self.dato.unidad and self.dato.unidad != "°C":
            text_unidad = self.canvas.create_text(
                self.x + 220.0,
                self.y + 130.0,
                anchor="nw",
                text=self.dato.unidad,
                fill="#FFFFFF",
                font=("ArialMT", 20)
            )
            self.elements.append(text_unidad)
        elif self.dato.unidad == "°C":
            # Símbolo C para Celsius
            text_c = self.canvas.create_text(
                self.x + 180.0,
                self.y + 130.0,
                anchor="nw",
                text="C",
                fill="#FFFFFF",
                font=("ArialMT", 20)
            )
            self.elements.append(text_c)
        
        # Rango óptimo (si hay alarma configurada)
        if self.dato.alarma:
            rango_texto = f"Rango optimo: {self.dato.alarma.valor_minimo}{self.dato.unidad} a {self.dato.alarma.valor_maximo}{self.dato.unidad}"
            text_rango = self.canvas.create_text(
                self.x + 10.0,
                self.y + 201.0,
                anchor="nw",
                text=rango_texto,
                fill="#FFFFFF",
                font=("ArialMT", 12)
            )
            self.elements.append(text_rango)
    
    def _render_binario(self):
        """Renderiza widget para dato de tipo BINARIO"""
        # Determinar estado
        en_alarma, mensaje = self.dato.esta_en_alarma()
        
        # Colores según estado
        if en_alarma:
            color_barra = "#FF4444"  # Rojo - MAL
            estado_texto = "MAL"
        else:
            color_barra = "#44FF44"  # Verde - BIEN
            estado_texto = "BIEN"
        
        color_fondo = "#0E1D3A"
        
        # Fondo del widget
        rect_fondo = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill=color_fondo,
            outline=""
        )
        self.elements.append(rect_fondo)
        
        # Barra inferior con color de estado
        barra_height = 36.0
        rect_barra = self.canvas.create_rectangle(
            self.x, self.y + self.height - barra_height,
            self.x + self.width, self.y + self.height,
            fill=color_barra,
            outline=""
        )
        self.elements.append(rect_barra)
        
        # Label del nombre del dato (CORREGIDO: de 24 a 16)
        text_nombre = self.canvas.create_text(
            self.x + 21.0,
            self.y + self.height - barra_height + 4.0,
            anchor="nw",
            text=self.dato.nombre,
            fill="#FFFFFF",
            font=("ArialMT", 16)
        )
        self.elements.append(text_nombre)
        
        # Estado principal (grande) (CORREGIDO: de 64 a 48)
        text_estado = self.canvas.create_text(
            self.x + self.width / 2,
            self.y + 140.0,
            anchor="center",
            text=estado_texto,
            fill="#FFFFFF",
            font=("Arial BoldMT", 48)
        )
        self.elements.append(text_estado)
        
        # Ícono o indicador visual (círculo de estado)
        circulo_size = 40
        circulo_x = self.x + self.width / 2
        circulo_y = self.y + 80.0
        
        circulo = self.canvas.create_oval(
            circulo_x - circulo_size / 2,
            circulo_y - circulo_size / 2,
            circulo_x + circulo_size / 2,
            circulo_y + circulo_size / 2,
            fill=color_barra,
            outline="#FFFFFF",
            width=3
        )
        self.elements.append(circulo)
    
    def update(self):
        """Actualiza el widget con los valores actuales del dato"""
        self.destroy()
        self.render()
    
    def destroy(self):
        """Elimina todos los elementos visuales del widget"""
        for element in self.elements:
            self.canvas.delete(element)
        self.elements.clear()


class WidgetGrid:
    """Gestor de grid para organizar múltiples widgets"""
    
    def __init__(self, canvas: Canvas, start_x: float = 361.0, 
                 start_y: float = 54.0, cols: int = 3, 
                 spacing_x: float = 20.0, spacing_y: float = 20.0):
        """
        Inicializa el grid de widgets
        
        Args:
            canvas: Canvas donde se dibujarán los widgets
            start_x, start_y: Posición inicial del grid
            cols: Número de columnas
            spacing_x, spacing_y: Espaciado entre widgets
        """
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.cols = cols
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.widgets: list[Widget] = []
        self.widget_width = 305.0
        self.widget_height = 290.0
    
    def add_widget(self, dato: Dato) -> Widget:
        """Agrega un widget al grid basado en un dato"""
        index = len(self.widgets)
        row = index // self.cols
        col = index % self.cols
        
        x = self.start_x + col * (self.widget_width + self.spacing_x)
        y = self.start_y + row * (self.widget_height + self.spacing_y)
        
        widget = Widget(self.canvas, dato, x, y, self.widget_width, self.widget_height)
        widget.render()
        self.widgets.append(widget)
        
        return widget
    
    def update_all(self):
        """Actualiza todos los widgets"""
        for widget in self.widgets:
            widget.update()
    
    def clear(self):
        """Elimina todos los widgets"""
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
    
    def refresh_from_datos(self, datos: list[Dato]):
        """Reconstruye el grid con una lista de datos"""
        self.clear()
        for dato in datos:
            self.add_widget(dato)
