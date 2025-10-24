"""
Historial Frame - Visualización del historial de eventos y alarmas con scroll
"""
from tkinter import Canvas, Frame, Scrollbar, Label
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from utils.navigation import nav
from models.historial__manager import get_historial_reciente


class HistorialFrame(BaseFrame):
    """Frame para mostrar el historial de eventos y alarmas con scroll"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame5"
        self.sidebar = None
        self.scroll_canvas = None
        self.scroll_frame = None
    
    def build(self):
        """Construye la UI del frame de historial"""
        user_data = nav.get_user_data()
        username = user_data.get('username', 'Nombre Apellido')   
        
        # Sidebar
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
        
        # Área principal con color de fondo
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
        
        # Headers fijos
        self.create_headers()
        
        # Scrollable canvas para eventos
        self.scroll_canvas = Canvas(self.master, bg="#153573", highlightthickness=0)
        self.scroll_canvas.place(x=368, y=180, width=1030, height=800)
        
        scrollbar = Scrollbar(self.master, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.place(x=1398, y=180, height=800)
        
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.scroll_frame = Frame(self.scroll_canvas, bg="#153573")
        self.scroll_canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")
        
        self.scroll_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        
        # Mostrar historial
        self.render_historial()
        
        # Activar refresco automático cada 5 segundos
        self.auto_refresh()

    def auto_refresh(self, intervalo_ms=5000):
        """Refresca la tabla automáticamente cada X milisegundos"""
        self.render_historial()
        self.after(intervalo_ms, self.auto_refresh)
    
    def create_headers(self):
        """Crea los encabezados de la tabla"""
        self.canvas.create_rectangle(
            410.0, 140.0, 1333.0, 180.0,
            fill="#152D5D",
            outline=""
        )
        headers = ["Dato", "Valor", "Importancia", "Hora Detección", "Mensaje"]
        positions = [432.0, 600.0, 750.0, 920.0, 1100.0]
        for header, x_pos in zip(headers, positions):
            self.canvas.create_text(
                x_pos, 150.0,
                anchor="nw",
                text=header,
                fill="#FFFFFF",
                font=("ArialMT", 20)
            )
    
    def render_historial(self):
        """Renderiza los eventos del historial dentro del scroll frame"""
        # Limite None = todos los eventos
        eventos = get_historial_reciente(limite=None)
        
        # Limpiar contenido previo
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not eventos:
            Label(self.scroll_frame, text="No hay eventos registrados en el historial",
                  fg="#FFFFFF", bg="#153573", font=("ArialMT", 24)).pack(pady=200)
            return
        
        row_height = 50
        for i, evento in enumerate(eventos):
            bg_color = "#152D5D" if i % 2 == 0 else "#1a3568"
            row_frame = Frame(self.scroll_frame, bg=bg_color, height=row_height)
            row_frame.pack(fill="x")
            
            # Dato
            Label(row_frame, text=evento.get('dato', ''), bg=bg_color, fg="#FFFFFF",
                  font=("ArialMT", 16), width=15, anchor="w").pack(side="left")
            # Valor
            Label(row_frame, text=evento.get('valor_registrado', ''), bg=bg_color,
                  fg="#FF4444", font=("ArialMT", 16), width=10, anchor="w").pack(side="left")
            # Importancia
            importancia_color = {
                'Normal': '#FFFFFF',
                'Importante': '#F8BC04',
                'Crítico': '#FF4444'
            }.get(evento.get('importancia', 'Normal'), '#FFFFFF')
            Label(row_frame, text=evento.get('importancia', ''), bg=bg_color,
                  fg=importancia_color, font=("ArialMT", 16), width=15, anchor="w").pack(side="left")
            # Hora
            Label(row_frame, text=evento.get('hora', ''), bg=bg_color,
                  fg="#FFFFFF", font=("ArialMT", 16), width=20, anchor="w").pack(side="left")
            # Mensaje
            mensaje = evento.get('mensaje', '')
            mensaje = mensaje[:30] + "..." if len(mensaje) > 30 else mensaje
            Label(row_frame, text=mensaje, bg=bg_color, fg="#FFFFFF",
                  font=("ArialMT", 14), width=30, anchor="w").pack(side="left")
    
    def refresh(self):
        """Refresca el frame actual"""
        self.render_historial()
    
    # Métodos de navegación
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
