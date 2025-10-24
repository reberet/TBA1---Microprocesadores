"""
Datos Frame - Vista de lista de todos los datos
"""
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from models import dato_manager
from utils.navigation import nav

class DatosFrame(BaseFrame):
    """Frame para mostrar datos en formato de lista"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame4"
        self.sidebar = None
    
    def build(self):
        """Construye la UI del frame de datos"""
        user_data = nav.get_user_data()
        username = user_data.get('username', 'Nombre Apellido')
        
        # Crear sidebar (con navegación automática)
        self.sidebar = Sidebar(self.canvas, self.image_manager, 
                              self.frame_name, username)
        self.sidebar.create()
        
        # Área principal
        self.canvas.create_rectangle(
            340.0, 30.0, 1280.0, 988.0,
            fill="#153573",
            outline=""
        )
        
        # Renderizar contenido
        self.render_datos()
        
        # Auto-refresh cada 2 segundos
        self.schedule_refresh()
    
    def schedule_refresh(self):
        """Programa el auto-refresh cada 2 segundos"""
        if self.window and self.window.winfo_exists():
            # Limpiar canvas antes de redibujar (excepto sidebar)
            self.canvas.delete("datos")
            self.render_datos()
            self.window.after(2000, self.schedule_refresh)
    
    def render_datos(self):
        """Renderiza la tabla con tag para poder borrarla"""
        
        # Título
        self.canvas.create_text(
            380.0, 70.0,
            anchor="w",
            text="Lista de Datos del Sistema",
            fill="#FFFFFF",
            font=("Arial BoldMT", 32),
            tags="datos"
        )
        
        # Headers
        self.canvas.create_rectangle(
            370.0, 130.0, 1250.0, 180.0,
            fill="#142D5D",
            outline="",
            tags="datos"
        )
        
        self.canvas.create_text(400.0, 155.0, anchor="w", text="Nombre", fill="#FFFFFF", font=("Arial BoldMT", 16), tags="datos")
        self.canvas.create_text(620.0, 155.0, anchor="w", text="Valor Actual", fill="#FFFFFF", font=("Arial BoldMT", 16), tags="datos")
        self.canvas.create_text(780.0, 155.0, anchor="w", text="Tipo", fill="#FFFFFF", font=("Arial BoldMT", 16), tags="datos")
        self.canvas.create_text(950.0, 155.0, anchor="w", text="Estado", fill="#FFFFFF", font=("Arial BoldMT", 16), tags="datos")
        
        # Datos
        datos = dato_manager.get_datos_activos()
        
        if not datos:
            self.canvas.create_text(
                810.0, 400.0,
                text="No hay datos configurados",
                fill="#FFFFFF",
                font=("ArialMT", 24),
                anchor="center",
                tags="datos"
            )
            return
        
        row_height = 70.0
        start_y = 200.0
        
        for i, dato in enumerate(datos):
            y_pos = start_y + (i * row_height)
            
            # Color alternado
            fill_color = "#152D5D" if i % 2 == 0 else "#1a3568"
            self.canvas.create_rectangle(
                370.0, y_pos, 1250.0, y_pos + 60.0,
                fill=fill_color,
                outline="",
                tags="datos"
            )
            
            # Nombre
            self.canvas.create_text(
                400.0, y_pos + 30.0,
                anchor="w",
                text=dato.nombre,
                fill="#FFFFFF",
                font=("ArialMT", 16),
                tags="datos"
            )
            
            # Valor (rojo si alarma, verde si ok)
            en_alarma, mensaje = dato.esta_en_alarma()
            valor_color = "#FF4444" if en_alarma else "#44FF44"
            self.canvas.create_text(
                620.0, y_pos + 30.0,
                anchor="w",
                text=dato.get_valor_formateado(),
                fill=valor_color,
                font=("Arial BoldMT", 16),
                tags="datos"
            )
            
            # Tipo
            tipo_texto = "Rango" if dato.tipo.value == "rango" else "Binario"
            self.canvas.create_text(
                780.0, y_pos + 30.0,
                anchor="w",
                text=tipo_texto,
                fill="#FFFFFF",
                font=("ArialMT", 16),
                tags="datos"
            )
            
            # Estado visual
            if en_alarma:
                self.canvas.create_rectangle(
                    940.0, y_pos + 12.0, 1120.0, y_pos + 48.0,
                    fill="#FF4444",
                    outline="",
                    tags="datos"
                )
                self.canvas.create_text(
                    1030.0, y_pos + 30.0,
                    text="⚠️ ALARMA",
                    fill="#FFFFFF",
                    font=("Arial BoldMT", 14),
                    tags="datos"
                )
            else:
                self.canvas.create_rectangle(
                    940.0, y_pos + 12.0, 1120.0, y_pos + 48.0,
                    fill="#44CC44",
                    outline="",
                    tags="datos"
                )
                self.canvas.create_text(
                    1030.0, y_pos + 30.0,
                    text="✓ OK",
                    fill="#FFFFFF",
                    font=("Arial BoldMT", 14),
                    tags="datos"
                )

def datos():
    """Función de conveniencia para iniciar el frame"""
    DatosFrame().show()
