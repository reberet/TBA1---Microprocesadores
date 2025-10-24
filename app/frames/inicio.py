"""
Inicio Frame - Pantalla inicial de bienvenida
"""
from tkinter import Button
from frames.base_frame import BaseFrame
from utils.navigation import nav

class InicioFrame(BaseFrame):
    """Frame de inicio/bienvenida de la aplicación"""
    
    def __init__(self):
        super().__init__(bg_color="#153573")
        self.frame_name = "frame0"
    
    def build(self):
        """Construye la UI del frame de inicio"""
        # Primero llenar todo el canvas con el color de fondo
        self.canvas.create_rectangle(
            0, 0, 
            self.width, self.height,
            fill="#153573",
            outline=""
        )
        
        # Imagen de fondo principal
        try:
            bg_image = self.image_manager.get_image(self.frame_name, "image_1.png")
            self.canvas.create_image(720.0, 512.0, image=bg_image)
            self.canvas.image1 = bg_image
        except FileNotFoundError:
            print("Advertencia: image_1.png no encontrada")
            # Si no hay imagen, ya tenemos el fondo azul
        
        # Logo Antel (arriba derecha)
        try:
            logo_antel = self.image_manager.get_image(self.frame_name, "image_2.png")
            self.canvas.create_image(1185.0, 63.0, image=logo_antel)
            self.canvas.image2 = logo_antel
        except FileNotFoundError:
            pass
        
        # Logo UCU (arriba derecha)
        try:
            logo_ucu = self.image_manager.get_image(self.frame_name, "image_3.png")
            self.canvas.create_image(1340.0, 68.0, image=logo_ucu)
            self.canvas.image3 = logo_ucu
        except FileNotFoundError:
            pass
        
        # Título principal - UNA SOLA LÍNEA
        self.canvas.create_text(
            138.0, 
            360.0,
            anchor="nw",
            text="MANTEL DATACENTER'S",
            fill="#FFFFFF",
            font=("Arial BoldMT", 76)
        )
        
        # Subtítulo - Primera línea
        self.canvas.create_text(
            138.0, 
            490.0,
            anchor="nw",
            text="Un ecosistema de soluciones digitales para",
            fill="#FFFFFF",
            font=("ArialMT", 24)
        )
        
        # Subtítulo - Segunda línea
        self.canvas.create_text(
            138.0, 
            530.0,
            anchor="nw",
            text="impulsar el desarrollo de tu negocio",
            fill="#FFFFFF",
            font=("ArialMT", 24)
        )
        
        # Botón INICIAR
        try:
            btn_iniciar_img = self.image_manager.get_image(self.frame_name, "button_1.png")
            btn_iniciar = Button(
                image=btn_iniciar_img,
                borderwidth=0,
                highlightthickness=0,
                command=self.go_to_login,
                relief="flat",
                cursor="hand2"
            )
            btn_iniciar.image = btn_iniciar_img
            btn_iniciar.place(x=138.0, y=620.0, width=197.0, height=38.0)
        except FileNotFoundError:
            # Fallback: crear botón de texto
            btn_iniciar = Button(
                text="INICIAR",
                bg="#F8BC04",
                fg="#000000",
                font=("Arial BoldMT", 16),
                borderwidth=0,
                command=self.go_to_login,
                cursor="hand2"
            )
            btn_iniciar.place(x=138.0, y=620.0, width=197.0, height=38.0)
    
    def go_to_login(self):
        """Navega al frame de login"""
        from frames.login import LoginFrame
        nav.navigate_to(lambda: LoginFrame().show())

def inicio():
    """Función de conveniencia para iniciar el frame"""
    InicioFrame().show()
