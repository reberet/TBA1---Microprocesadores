"""
Conexiones Frame - Configuración de conexiones WIFI y USB
"""
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from utils.navigation import nav

class ConexionesFrame(BaseFrame):
    """Frame para gestionar conexiones WIFI y USB"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame6"
        self.sidebar = None
    
    def build(self):
        """Construye la UI del frame de conexiones"""
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
            on_historial=self.go_to_historial,
            on_conexiones=self.refresh,
            on_logout=self.logout
        )
        
        # Área principal
        self.canvas.create_rectangle(
            369.0, 28.0, 1399.0, 986.0,
            fill="#153573",
            outline=""
        )
        
        # Título
        self.canvas.create_text(
            600.0, 80.0,
            anchor="nw",
            text="Configuración de Conexiones",
            fill="#FFFFFF",
            font=("Arial BoldMT", 36)
        )
        
        # Widget WIFI
        self.create_wifi_widget()
        
        # Widget USB
        self.create_usb_widget()
    
    def create_wifi_widget(self):
        """Crea el widget de conexión WIFI"""
        # Título WIFI
        self.canvas.create_text(
            656.0, 200.0,
            anchor="nw",
            text="WIFI",
            fill="#FFFFFF",
            font=("Arial BoldMT", 40)
        )
        
        # Contenedor WIFI
        self.canvas.create_rectangle(
            532.0, 260.0, 863.0, 800.0,
            fill="#142D5D",
            outline=""
        )
        
        # Área de información WIFI
        self.canvas.create_rectangle(
            571.0, 303.0, 825.0, 760.0,
            fill="#D9D9D9",
            outline=""
        )
        
        # Información de estado (placeholder)
        self.canvas.create_text(
            698.0, 400.0,
            text="Estado: Conectado\n\n"
                 "SSID: DataCenter_NET\n\n"
                 "IP: 192.168.1.100\n\n"
                 "Señal: Excelente",
            fill="#000000",
            font=("ArialMT", 16),
            anchor="center",
            justify="center"
        )
    
    def create_usb_widget(self):
        """Crea el widget de conexión USB"""
        # Título USB
        self.canvas.create_text(
            1020.0, 200.0,
            anchor="nw",
            text="USB",
            fill="#FFFFFF",
            font=("Arial BoldMT", 40)
        )
        
        # Contenedor USB
        self.canvas.create_rectangle(
            896.0, 260.0, 1227.0, 800.0,
            fill="#142D5D",
            outline=""
        )
        
        # Área de información USB
        self.canvas.create_rectangle(
            935.0, 303.0, 1189.0, 760.0,
            fill="#D9D9D9",
            outline=""
        )
        
        # Información de estado (placeholder)
        self.canvas.create_text(
            1062.0, 400.0,
            text="Estado: Conectado\n\n"
                 "Dispositivos: 2\n\n"
                 "- Sensor Temp\n"
                 "- Sensor Humedad\n\n"
                 "Puerto: USB3.0",
            fill="#000000",
            font=("ArialMT", 16),
            anchor="center",
            justify="center"
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
    
    def go_to_historial(self):
        from frames.historial import HistorialFrame
        nav.navigate_to(lambda: HistorialFrame().show())
    
    def logout(self):
        nav.clear_user_data()
        from frames.login import LoginFrame
        nav.navigate_to(lambda: LoginFrame().show())

def conexiones():
    """Función de conveniencia para iniciar el frame"""
    ConexionesFrame().show()
