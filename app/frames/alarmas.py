"""
Alarmas Frame - Vista de todas las alarmas configuradas
"""
from tkinter import Entry, Button
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from models import dato_manager
from utils.navigation import nav

class AlarmasFrame(BaseFrame):
    """Frame para ver y gestionar alarmas activas"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame3"
        self.sidebar = None
    
    def build(self):
        """Construye la UI del frame de alarmas"""
        user_data = nav.get_user_data()
        username = user_data.get('username', 'Nombre Apellido')
        
        # Crear sidebar
        self.sidebar = Sidebar(self.canvas, self.image_manager, 
                              self.frame_name, username)
        self.sidebar.create(
            on_dashboard=self.go_to_dashboard,
            on_datos=self.go_to_datos,
            on_alarmas=self.refresh,
            on_configurar=self.go_to_configurar,
            on_historial=self.go_to_historial,
            on_conexiones=self.go_to_conexiones,
            on_logout=self.logout
        )
        
        # Área principal
        self.canvas.create_rectangle(
            367.0, 30.0, 1397.0, 988.0,
            fill="#153573",
            outline=""
        )
        
        # Título
        self.canvas.create_text(
            500.0, 60.0,
            anchor="nw",
            text="Estado de Alarmas",
            fill="#FFFFFF",
            font=("Arial BoldMT", 32)
        )
        
        # Headers
        self.create_headers()
        
        # Mostrar alarmas activas
        self.render_alarmas()
    
    def create_headers(self):
        """Crea los encabezados de la tabla"""
        self.canvas.create_rectangle(
            414.0, 140.0, 1337.0, 180.0,
            fill="#142D5D",
            outline=""
        )
        
        self.canvas.create_text(
            432.0, 150.0,
            anchor="nw",
            text="Dato",
            fill="#FFFFFF",
            font=("ArialMT", 22)
        )
        
        self.canvas.create_text(
            650.0, 150.0,
            anchor="nw",
            text="Valor Actual",
            fill="#FFFFFF",
            font=("ArialMT", 22)
        )
        
        self.canvas.create_text(
            850.0, 150.0,
            anchor="nw",
            text="Rango/Estado Esperado",
            fill="#FFFFFF",
            font=("ArialMT", 22)
        )
        
        self.canvas.create_text(
            1150.0, 150.0,
            anchor="nw",
            text="Estado",
            fill="#FFFFFF",
            font=("ArialMT", 22)
        )
    
    def render_alarmas(self):
        """Renderiza todas las alarmas configuradas"""
        datos = dato_manager.get_datos_activos()
        
        if not datos:
            self.canvas.create_text(
                883.0, 400.0,
                text="No hay datos con alarmas configuradas",
                fill="#FFFFFF",
                font=("ArialMT", 24),
                anchor="center"
            )
            return
        
        row_height = 65.0
        start_y = 210.0
        
        for i, dato in enumerate(datos):
            if not dato.alarma:
                continue
                
            y_pos = start_y + (i * row_height)
            
            # Verificar si está en alarma
            en_alarma, mensaje = dato.esta_en_alarma()
            
            # Fondo de fila
            fill_color = "#FF4444" if en_alarma else "#152D5D"
            self.canvas.create_rectangle(
                414.0, y_pos, 1337.0, y_pos + 55.0,
                fill=fill_color,
                outline=""
            )
            
            # Nombre del dato
            self.canvas.create_text(
                432.0, y_pos + 15.0,
                anchor="nw",
                text=dato.nombre,
                fill="#FFFFFF",
                font=("ArialMT", 18)
            )
            
            # Valor actual
            self.canvas.create_text(
                650.0, y_pos + 15.0,
                anchor="nw",
                text=dato.get_valor_formateado(),
                fill="#FFFFFF",
                font=("Arial BoldMT", 18)
            )
            
            # Rango/Estado esperado
            if dato.tipo.value == "rango":
                rango_texto = f"{dato.alarma.valor_minimo}{dato.unidad} - {dato.alarma.valor_maximo}{dato.unidad}"
            else:
                rango_texto = f"Esperado: {dato.alarma.estado_esperado.value.upper()}"
            
            self.canvas.create_text(
                850.0, y_pos + 15.0,
                anchor="nw",
                text=rango_texto,
                fill="#FFFFFF",
                font=("ArialMT", 18)
            )
            
            # Estado
            estado_texto = "⚠️ ALARMA" if en_alarma else "✓ OK"
            self.canvas.create_text(
                1150.0, y_pos + 15.0,
                anchor="nw",
                text=estado_texto,
                fill="#FFFFFF",
                font=("Arial BoldMT", 18)
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
    
    def go_to_configurar(self):
        from frames.configurar_datos import ConfigurarDatosFrame
        nav.navigate_to(lambda: ConfigurarDatosFrame().show())
    
    def go_to_historial(self):
        from frames.historial import HistorialFrame
        nav.navigate_to(lambda: HistorialFrame().show())
    
    def go_to_conexiones(self):
        from frames.conexiones import ConexionesFrame
        nav.navigate_to(lambda: ConexionesFrame().show())
    
    def logout(self):
        nav.clear_user_data()
        from frames.login import LoginFrame
        nav.navigate_to(lambda: LoginFrame().show())

def alarmas():
    """Función de conveniencia para iniciar el frame"""
    AlarmasFrame().show()
