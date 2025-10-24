"""
Sidebar Component - Barra lateral reutilizable con 6 opciones de navegación
"""
from tkinter import Canvas, Button
from typing import Callable, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from utils.image_manager import ImageManager

class Sidebar:
    """Componente de barra lateral con navegación completa"""
    
    def __init__(self, canvas: Canvas, image_manager: 'ImageManager', 
                 frame_name: str, username: str = "Nombre Apellido"):
        self.canvas = canvas
        self.image_manager = image_manager
        self.frame_name = frame_name
        self.username = username
        self.buttons = []
        
    def create(self, on_dashboard: Optional[Callable] = None, 
               on_datos: Optional[Callable] = None,
               on_alarmas: Optional[Callable] = None, 
               on_configurar: Optional[Callable] = None, 
               on_historial: Optional[Callable] = None, 
               on_conexiones: Optional[Callable] = None,
               on_logout: Optional[Callable] = None):
        """
        Crea el sidebar completo con todos sus elementos
        Si no se proporcionan callbacks, usa navegación automática por defecto
        
        Args:
            on_dashboard: Callback para Dashboard (opcional)
            on_datos: Callback para Lista de Datos (opcional)
            on_alarmas: Callback para Alarmas (opcional)
            on_configurar: Callback para Configurar Datos (opcional)
            on_historial: Callback para Historial (opcional)
            on_conexiones: Callback para Conexiones (opcional)
            on_logout: Callback para cerrar sesión (opcional)
        """
        # Usar navegación por defecto si no se proporcionan callbacks
        on_dashboard = on_dashboard or self._go_to_dashboard
        on_datos = on_datos or self._go_to_datos
        on_alarmas = on_alarmas or self._go_to_alarmas
        on_configurar = on_configurar or self._go_to_configurar
        on_historial = on_historial or self._go_to_historial
        on_conexiones = on_conexiones or self._go_to_conexiones
        on_logout = on_logout or self._logout
        
        # Rectángulo principal del sidebar
        self.canvas.create_rectangle(
            0.0, 0.0, 323.0, 1024.0,
            fill="#153573",
            outline=""
        )
        
        # Rectángulo inferior (zona de logout)
        self.canvas.create_rectangle(
            0.0, 952.0, 323.0, 1024.0,
            fill="#0C2658",
            outline=""
        )
        
        # Nombre del usuario
        self.canvas.create_text(
            44.0, 112.0,
            anchor="nw",
            text=self.username,
            fill="#FFFFFF",
            font=("ArialMT", 32)
        )
        
        # Posiciones Y para los botones del menú (6 botones)
        button_start_y = 200.0
        button_height = 41.0
        button_spacing = 51.0  # Altura del botón + espacio
        
        # Botón 1: Dashboard
        self._create_standard_button(
            text="Dashboard",
            callback=on_dashboard,
            y_position=button_start_y
        )
        
        # Botón 2: Datos
        self._create_standard_button(
            text="Datos",
            callback=on_datos,
            y_position=button_start_y + button_spacing
        )
        
        # Botón 3: Alarmas
        self._create_standard_button(
            text="Alarmas",
            callback=on_alarmas,
            y_position=button_start_y + button_spacing * 2
        )
        
        # Botón 4: Configurar Datos
        self._create_standard_button(
            text="Configurar Datos",
            callback=on_configurar,
            y_position=button_start_y + button_spacing * 3
        )
        
        # Botón 5: Historial
        self._create_standard_button(
            text="Historial",
            callback=on_historial,
            y_position=button_start_y + button_spacing * 4
        )
        
        # Botón 6: Conexiones
        self._create_standard_button(
            text="Conexiones",
            callback=on_conexiones,
            y_position=button_start_y + button_spacing * 5
        )
        
        # Botón de cerrar sesión (formato especial, más pequeño, abajo)
        self._create_logout_button(
            callback=on_logout
        )
    
    def _create_standard_button(self, text: str, callback: Callable, y_position: float):
        """
        Crea un botón estándar del menú con formato consistente
        
        Args:
            text: Texto del botón
            callback: Función a ejecutar al hacer click
            y_position: Posición Y del botón
        """
        btn = Button(
            text=text,
            bg="#142D5D",
            fg="#FFFFFF",
            font=("ArialMT", 18),
            borderwidth=0,
            command=callback,
            cursor="hand2",
            activebackground="#1a3568",
            activeforeground="#FFFFFF",
            relief="flat",
            anchor="w",
            padx=40
        )
        btn.place(x=0.0, y=y_position, width=323.0, height=41.0)
        self.buttons.append(btn)
    
    def _create_logout_button(self, callback: Callable):
        """
        Crea el botón de cerrar sesión con formato especial
        
        Args:
            callback: Función a ejecutar al hacer click
        """
        btn = Button(
            text="🚪 Cerrar Sesión",
            bg="#0C2658",
            fg="#FFFFFF",
            font=("ArialMT", 16),
            borderwidth=0,
            command=callback,
            cursor="hand2",
            activebackground="#081b3f",
            activeforeground="#FFFFFF",
            relief="flat"
        )
        btn.place(x=68.0, y=973.0, width=185.0, height=36.0)
        self.buttons.append(btn)
    
    # ============ MÉTODOS DE NAVEGACIÓN POR DEFECTO ============
    
    def _go_to_dashboard(self):
        """Navegación por defecto al dashboard"""
        from utils.navigation import nav
        from frames.dashboard import DashboardFrame
        nav.navigate_to(lambda: DashboardFrame().show())
    
    def _go_to_datos(self):
        """Navegación por defecto a datos"""
        from utils.navigation import nav
        from frames.datos import DatosFrame
        nav.navigate_to(lambda: DatosFrame().show())
    
    def _go_to_alarmas(self):
        """Navegación por defecto a alarmas"""
        from utils.navigation import nav
        from frames.alarmas import AlarmasFrame
        nav.navigate_to(lambda: AlarmasFrame().show())
    
    def _go_to_configurar(self):
        """Navegación por defecto a configurar"""
        from utils.navigation import nav
        from frames.configurar_datos import ConfigurarDatosFrame
        nav.navigate_to(lambda: ConfigurarDatosFrame().show())
    
    def _go_to_historial(self):
        """Navegación por defecto a historial"""
        from utils.navigation import nav
        from frames.historial import HistorialFrame
        nav.navigate_to(lambda: HistorialFrame().show())
    
    def _go_to_conexiones(self):
        """Navegación por defecto a conexiones"""
        from utils.navigation import nav
        from frames.conexiones import ConexionesFrame
        nav.navigate_to(lambda: ConexionesFrame().show())
    
    def _logout(self):
        """Logout por defecto"""
        from utils.navigation import nav
        nav.clear_user_data()
        from frames.login import LoginFrame
        nav.navigate_to(lambda: LoginFrame().show())
    
    def destroy(self):
        """Destruye todos los botones del sidebar"""
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
