"""
Dashboard Frame - Panel principal con widgets dinámicos
"""
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from components.widget import WidgetGrid
from models import dato_manager
from utils.navigation import nav

class DashboardFrame(BaseFrame):
    """Frame principal del dashboard con widgets"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame2"
        self.sidebar = None
        self.widget_grid = None
        self.update_job = None
    
    def build(self):
        """Construye la UI del dashboard"""
        user_data = nav.get_user_data()
        username = user_data.get('username', 'Usuario')
        
        # Crear sidebar
        self.sidebar = Sidebar(self.canvas, self.image_manager, 
                              self.frame_name, username)
        self.sidebar.create(
            on_dashboard=self.refresh,
            on_datos=lambda: print("Datos - TODO"),
            on_alarmas=lambda: print("Alarmas - TODO"),
            on_configurar=lambda: print("Configurar - TODO"),
            on_historial=lambda: print("Historial - TODO"),
            on_conexiones=lambda: print("Conexiones - TODO"),
            on_logout=self.logout
        )
        
        # Crear grid de widgets
        self.widget_grid = WidgetGrid(
            canvas=self.canvas,
            start_x=361.0,
            start_y=54.0,
            cols=3,
            spacing_x=20.0,
            spacing_y=20.0
        )
        
        # Cargar datos y crear widgets
        self.cargar_widgets()
        
        # Iniciar actualización automática
        self.start_auto_update()
    
    def cargar_widgets(self):
        """Carga los datos y crea los widgets"""
        datos = dato_manager.get_datos_activos()
        
        if datos:
            self.widget_grid.refresh_from_datos(datos)
            print(f"✅ Cargados {len(datos)} widgets")
        else:
            print("⚠️  No hay datos para mostrar")
    
    def refresh(self):
        """Refresca los widgets manualmente"""
        
        self.cargar_widgets()
    
    def start_auto_update(self):
        """Inicia actualización automática cada 2 segundos"""
        self.auto_update()
    
    def auto_update(self):
        """Actualiza los datos automáticamente"""
        try:
            self.cargar_widgets()
            
            # Programar siguiente actualización
            if self.window and self.window.winfo_exists():
                self.update_job = self.window.after(2000, self.auto_update)
        except Exception as e:
            print(f"❌ Error en auto_update: {e}")
    
    def logout(self):
        """Cierra sesión"""
        nav.clear_user_data()
        from frames.login import LoginFrame
        nav.navigate_to(lambda: LoginFrame().show())

def dashboard():
    """Función para iniciar el dashboard"""
    DashboardFrame().show()
