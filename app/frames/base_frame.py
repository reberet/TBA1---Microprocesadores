"""
Base Frame - Clase base para todos los frames de la aplicación
"""
from tkinter import Tk, Canvas
from pathlib import Path
from abc import ABC, abstractmethod
from utils.image_manager import ImageManager
from utils.navigation import nav

class BaseFrame(ABC):
    """Clase base abstracta para todos los frames"""
    
    def __init__(self, width: int = 1440, height: int = 1024, 
                 bg_color: str = "#153573"):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.window: Tk = None
        self.canvas: Canvas = None
        self.image_manager = ImageManager()
        
    def create_window(self):
        """Crea y configura la ventana principal"""
        self.window = Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(bg=self.bg_color)
        self.window.resizable(False, False)
        
        # Eliminar bordes y padding
        self.window.overrideredirect(False)  # Mantener controles de ventana
        
        # Registrar ventana en el navegador
        nav.set_current_window(self.window)
        
        return self.window
    
    def create_canvas(self) -> Canvas:
        """Crea el canvas principal del frame"""
        self.canvas = Canvas(
            self.window,
            bg=self.bg_color,
            height=self.height,
            width=self.width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        return self.canvas
    
    @abstractmethod
    def build(self):
        """Método abstracto que debe implementar cada frame para construir su UI"""
        pass
    
    def run(self):
        """Ejecuta el mainloop de la ventana"""
        if self.window:
            self.window.mainloop()
    
    def show(self):
        """Método principal para mostrar el frame"""
        self.create_window()
        self.create_canvas()
        self.build()
        self.run()
