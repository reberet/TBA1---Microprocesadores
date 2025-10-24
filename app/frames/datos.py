"""
Datos Frame - Vista de lista de todos los datos con scroll
"""
from tkinter import Frame, Scrollbar, Canvas
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from models import dato_manager
from utils.navigation import nav

class DatosFrame(BaseFrame):
    """Frame para mostrar datos en formato de lista con scroll"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame4"
        self.sidebar = None
        self.scroll_frame = None
        self.datos_canvas = None
    
    def build(self):
        """Construye la UI del frame de datos"""
        user_data = nav.get_user_data()
        username = user_data.get('username', 'Nombre Apellido')
        
        # Crear sidebar
        self.sidebar = Sidebar(self.canvas, self.image_manager, 
                              self.frame_name, username)
        self.sidebar.create(
            on_dashboard=self.go_to_dashboard,
            on_datos=self.refresh,
            on_alarmas=self.go_to_alarmas,
            on_configurar=self.go_to_configurar,
            on_historial=self.go_to_historial,
            on_conexiones=self.go_to_conexiones,
            on_logout=self.logout
        )
        
        # Área principal con scroll
        self.create_scrollable_area()
        
        # Cargar y mostrar datos
        self.render_datos()
        
        # Auto-refresh cada 2 segundos
        self.schedule_refresh()
    
    def create_scrollable_area(self):
        """Crea el área scrolleable para la tabla"""
        # Contenedor principal
        container = Frame(self.canvas, bg="#153573")
        container.place(x=367.0, y=30.0, width=1030.0, height=958.0)
        
        # Canvas para scroll
        self.datos_canvas = Canvas(container, bg="#153573", highlightthickness=0)
        scrollbar = Scrollbar(container, orient="vertical", command=self.datos_canvas.yview)
        self.scroll_frame = Frame(self.datos_canvas, bg="#153573")
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.datos_canvas.configure(scrollregion=self.datos_canvas.bbox("all"))
        )
        
        self.datos_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.datos_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.datos_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def render_datos(self):
        """Renderiza la tabla de datos"""
        # Limpiar contenido anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Título
        title_canvas = Canvas(self.scroll_frame, bg="#153573", height=50, highlightthickness=0)
        title_canvas.pack(fill="x", padx=20, pady=(10, 20))
        title_canvas.create_text(
            10, 25,
            anchor="w",
            text="Lista de Datos del Sistema",
            fill="#FFFFFF",
            font=("Arial BoldMT", 28)
        )
        
        # Headers
        header_canvas = Canvas(self.scroll_frame, bg="#142D5D", height=50, highlightthickness=0)
        header_canvas.pack(fill="x", padx=20, pady=(0, 5))
        
        header_canvas.create_text(30, 25, anchor="w", text="Nombre", fill="#FFFFFF", font=("Arial BoldMT", 18))
        header_canvas.create_text(280, 25, anchor="w", text="Valor Actual", fill="#FFFFFF", font=("Arial BoldMT", 18))
        header_canvas.create_text(480, 25, anchor="w", text="Tipo", fill="#FFFFFF", font=("Arial BoldMT", 18))
        header_canvas.create_text(650, 25, anchor="w", text="Unidad", fill="#FFFFFF", font=("Arial BoldMT", 18))
        header_canvas.create_text(800, 25, anchor="w", text="Importancia", fill="#FFFFFF", font=("Arial BoldMT", 18))
        
        # Datos
        datos = dato_manager.get_datos_activos()
        
        if not datos:
            no_data = Canvas(self.scroll_frame, bg="#153573", height=200, highlightthickness=0)
            no_data.pack(fill="x", padx=20, pady=50)
            no_data.create_text(
                500, 100,
                text="No hay datos configurados\nLos datos UDP se crearán automáticamente",
                fill="#FFFFFF",
                font=("ArialMT", 20),
                justify="center"
            )
            return
        
        for i, dato in enumerate(datos):
            # Color alternado
            fill_color = "#152D5D" if i % 2 == 0 else "#1a3568"
            
            row_canvas = Canvas(self.scroll_frame, bg=fill_color, height=60, highlightthickness=0)
            row_canvas.pack(fill="x", padx=20, pady=2)
            
            # Nombre
            row_canvas.create_text(
                30, 30,
                anchor="w",
                text=dato.nombre,
                fill="#FFFFFF",
                font=("ArialMT", 16)
            )
            
            # Valor (rojo si está en alarma)
            en_alarma, _ = dato.esta_en_alarma()
            valor_color = "#FF4444" if en_alarma else "#FFFFFF"
            row_canvas.create_text(
                280, 30,
                anchor="w",
                text=dato.get_valor_formateado(),
                fill=valor_color,
                font=("Arial BoldMT", 16)
            )
            
            # Tipo
            tipo_texto = "Rango" if dato.tipo.value == "rango" else "Binario"
            row_canvas.create_text(
                480, 30,
                anchor="w",
                text=tipo_texto,
                fill="#FFFFFF",
                font=("ArialMT", 16)
            )
            
            # Unidad
            row_canvas.create_text(
                650, 30,
                anchor="w",
                text=dato.unidad if dato.unidad else "-",
                fill="#FFFFFF",
                font=("ArialMT", 16)
            )
            
            # Importancia con color
            importancia_color = {
                'Normal': '#FFFFFF',
                'Importante': '#F8BC04',
                'Crítico': '#FF4444'
            }.get(dato.importancia, '#FFFFFF')
            
            row_canvas.create_text(
                800, 30,
                anchor="w",
                text=dato.importancia,
                fill=importancia_color,
                font=("Arial BoldMT", 16)
            )
            
            # Indicador de alarma
            if en_alarma:
                row_canvas.create_text(
                    950, 30,
                    anchor="w",
                    text="⚠️ ALARMA",
                    fill="#FF4444",
                    font=("Arial BoldMT", 14)
                )
    
    def schedule_refresh(self):
        """Programa el auto-refresh cada 2 segundos"""
        if self.window:
            self.render_datos()
            self.window.after(2000, self.schedule_refresh)
    
    def refresh(self):
        """Refresca manualmente"""
        self.render_datos()
    
    def go_to_dashboard(self):
        from frames.dashboard import DashboardFrame
        nav.navigate_to(lambda: DashboardFrame().show())
    
    def go_to_alarmas(self):
        from frames.alarmas import AlarmasFrame
        nav.navigate_to(lambda: AlarmasFrame().show())
    
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

def datos():
    """Función de conveniencia para iniciar el frame"""
    DatosFrame().show()
