"""
Historial Frame - Visualización del historial de eventos y alarmas
"""
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from models import dato_manager
from utils.navigation import nav

class HistorialFrame(BaseFrame):
    """Frame para mostrar el historial de eventos y alarmas"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame5"
        self.sidebar = None
    
    def build(self):
        """Construye la UI del frame de historial"""
        user_data = nav.get_user_data()
        username = user_data.get('username', 'Nombre Apellido')
        
        # Crear sidebar
        self.sidebar = Sidebar(self.canvas, self.image_manager, 
                              self.frame_name, username)
        self.sidebar.create(
            on_dashboard=self.go_to_dashboard,
            on_datos=self.go_to_datos,
            on_alarmas=self.go_to_alarmas,
            on_configurar=self.go_to_configurar,
            on_historial=self.refresh,
            on_conexiones=self.go_to_conexiones,
            on_logout=self.logout
        )
        
        # Área principal
        self.canvas.create_rectangle(
            368.0, 31.0, 1398.0, 989.0,
            fill="#153573",
            outline=""
        )
        
        # Título
        self.canvas.create_text(
            500.0, 60.0,
            anchor="nw",
            text="Historial de Eventos",
            fill="#FFFFFF",
            font=("Arial BoldMT", 32)
        )
        
        # Headers
        self.create_headers()
        
        # Mostrar historial
        self.render_historial()
    
    def create_headers(self):
        """Crea los encabezados de la tabla"""
        self.canvas.create_rectangle(
            410.0, 140.0, 1333.0, 180.0,
            fill="#152D5D",
            outline=""
        )
        
        self.canvas.create_text(
            432.0, 150.0,
            anchor="nw",
            text="Dato",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            600.0, 150.0,
            anchor="nw",
            text="Valor",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            750.0, 150.0,
            anchor="nw",
            text="Importancia",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            920.0, 150.0,
            anchor="nw",
            text="Hora Detección",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            1100.0, 150.0,
            anchor="nw",
            text="Mensaje",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
    
    def render_historial(self):
        """Renderiza los eventos del historial"""
        eventos = dato_manager.get_historial_reciente(limite=10)
        
        if not eventos:
            self.canvas.create_text(
                883.0, 400.0,
                text="No hay eventos registrados en el historial",
                fill="#FFFFFF",
                font=("ArialMT", 24),
                anchor="center"
            )
            return
        
        row_height = 60.0
        start_y = 210.0
        
        for i, evento in enumerate(eventos):
            y_pos = start_y + (i * row_height)
            
            # Fondo de fila (alternado)
            fill_color = "#152D5D" if i % 2 == 0 else "#1a3568"
            self.canvas.create_rectangle(
                410.0, y_pos, 1333.0, y_pos + 50.0,
                fill=fill_color,
                outline=""
            )
            
            # Dato
            self.canvas.create_text(
                432.0, y_pos + 15.0,
                anchor="nw",
                text=evento['dato'],
                fill="#FFFFFF",
                font=("ArialMT", 16)
            )
            
            # Valor registrado
            self.canvas.create_text(
                600.0, y_pos + 15.0,
                anchor="nw",
                text=evento['valor_registrado'],
                fill="#FF4444",
                font=("ArialMT", 16)
            )
            
            # Importancia
            importancia_color = {
                'Normal': '#FFFFFF',
                'Importante': '#F8BC04',
                'Crítico': '#FF4444'
            }.get(evento['importancia'], '#FFFFFF')
            
            self.canvas.create_text(
                750.0, y_pos + 15.0,
                anchor="nw",
                text=evento['importancia'],
                fill=importancia_color,
                font=("ArialMT", 16)
            )
            
            # Hora
            self.canvas.create_text(
                920.0, y_pos + 15.0,
                anchor="nw",
                text=evento['hora'],
                fill="#FFFFFF",
                font=("ArialMT", 16)
            )
            
            # Mensaje (truncado si es muy largo)
            mensaje = evento['mensaje'][:30] + "..." if len(evento['mensaje']) > 30 else evento['mensaje']
            self.canvas.create_text(
                1100.0, y_pos + 15.0,
                anchor="nw",
                text=mensaje,
                fill="#FFFFFF",
                font=("ArialMT", 14)
            )
    
    def refresh(self):
        """Refresca el frame actual"""
        pass
    
    def go_to_dashboard(self):
        from frames.dashboard import DashboardFrame
        nav.navigate_to(lambda: DashboardFrame().show())
    
    def go_to_datos(self):
        from frames.datos import DatosFrame
        nav.navigate_to(lambda: DatosFrame().show())
    
    def go_to_alarmas(self):
        from frames.alarmas import AlarmasFrame
        nav.navigate_to(lambda: AlarmasFrame().show())
    
    def go_to_configurar(self):
        from frames.configurar_datos import ConfigurarDatosFrame
        nav.navigate_to(lambda: ConfigurarDatosFrame().show())
    
    def go_to_conexiones(self):
        from frames.conexiones import ConexionesFrame
        nav.navigate_to(lambda: ConexionesFrame().show())
    
    def logout(self):
        nav.clear_user_data()
        from frames.login import LoginFrame
        nav.navigate_to(lambda: LoginFrame().show())

def historial():
    """Función de conveniencia para iniciar el frame"""
    HistorialFrame().show()
