"""
Navigation Manager - Maneja la navegación entre frames de la aplicación
"""
from typing import Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from tkinter import Tk

class NavigationManager:
    """Administrador de navegación entre frames"""
    
    def __init__(self):
        self.current_window: Optional['Tk'] = None
        self.user_data: dict = {}
    
    def set_current_window(self, window: 'Tk'):
        """Establece la ventana actual"""
        self.current_window = window
    
    def navigate_to(self, destination_func: Callable):
        """
        Navega a otro frame destruyendo el actual
        
        Args:
            destination_func: Función que crea el nuevo frame
        """
        if self.current_window:
            self.current_window.destroy()
        destination_func()
    
    def set_user_data(self, username: str, **kwargs):
        """
        Guarda datos del usuario después del login
        
        Args:
            username: Nombre de usuario
            **kwargs: Datos adicionales del usuario
        """
        self.user_data = {
            'username': username,
            **kwargs
        }
    
    def get_user_data(self) -> dict:
        """Obtiene los datos del usuario actual"""
        return self.user_data
    
    def clear_user_data(self):
        """Limpia los datos del usuario (logout)"""
        self.user_data.clear()

# Instancia global del navegador
nav = NavigationManager()
