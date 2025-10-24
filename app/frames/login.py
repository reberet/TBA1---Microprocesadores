"""
Login Frame - Pantalla de autenticación
"""
from tkinter import Button, Entry
from frames.base_frame import BaseFrame
from utils.navigation import nav
from backend.UDPserver.server import run_server
class LoginFrame(BaseFrame):
    """Frame de login/autenticación"""
    
    def __init__(self):
        super().__init__(bg_color="#153573")
        self.frame_name = "frame1"
        self.entry_usuario = None
        self.entry_password = None
    
    def build(self):
        """Construye la UI del frame de login"""
        # Imagen de fondo
        bg_image = self.image_manager.get_image(self.frame_name, "image_1.png")
        self.canvas.create_image(1080.0, 512.0, image=bg_image)
        self.canvas.image1 = bg_image
        
        # Logo principal (Iniciar Sesión)
        logo_main = self.image_manager.get_image(self.frame_name, "image_2.png")
        self.canvas.create_image(354.0, 248.0, image=logo_main)
        self.canvas.image2 = logo_main
        
        # Logo Antel
        logo_antel = self.image_manager.get_image(self.frame_name, "image_3.png")
        self.canvas.create_image(145.0, 922.0, image=logo_antel)
        self.canvas.image3 = logo_antel
        
        # Logo UCU
        logo_ucu = self.image_manager.get_image(self.frame_name, "image_4.png")
        self.canvas.create_image(554.0, 921.0, image=logo_ucu)
        self.canvas.image4 = logo_ucu
        
        # Label Usuario
        self.canvas.create_text(
            42.0, 397.0,
            anchor="nw",
            text="Usuario",
            fill="#FFFFFF",
            font=("Arial BoldMT", 24)
        )
        
        # Entry Usuario
        entry_img_1 = self.image_manager.get_image(self.frame_name, "entry_2.png")
        self.canvas.create_image(354.5, 468.0, image=entry_img_1)
        self.canvas.entry_bg_1 = entry_img_1
        
        self.entry_usuario = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_usuario.place(x=57.0, y=448.0, width=595.0, height=38.0)
        
        # Label Contraseña
        self.canvas.create_text(
            42.0, 541.0,
            anchor="nw",
            text="Contraseña",
            fill="#FFFFFF",
            font=("Arial BoldMT", 24)
        )
        
        # Entry Contraseña
        entry_img_2 = self.image_manager.get_image(self.frame_name, "entry_1.png")
        self.canvas.create_image(354.5, 611.0, image=entry_img_2)
        self.canvas.entry_bg_2 = entry_img_2
        
        self.entry_password = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            show="*"  # Ocultar contraseña
        )
        self.entry_password.place(x=57.0, y=591.0, width=595.0, height=38.0)
        
        # Botón Iniciar Sesión
        btn_login_img = self.image_manager.get_image(self.frame_name, "button_1.png")
        btn_login = Button(
            image=btn_login_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_login,
            relief="flat"
        )
        btn_login.image = btn_login_img
        btn_login.place(x=256.0, y=696.0, width=197.0, height=38.0)
        
        # Permitir login con Enter
        self.entry_password.bind('<Return>', lambda e: self.handle_login())
    
    def handle_login(self):
        """Maneja el proceso de login"""
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        # Aquí iría la validación real
        # Por ahora, aceptamos cualquier credencial
        if self.validate_credentials(usuario, password):
            # Guardar datos del usuario
            nav.set_user_data(usuario)
            
            # Navegar al dashboard
            self.iniciar_servidor_udp()
            from frames.dashboard import DashboardFrame
            nav.navigate_to(lambda: DashboardFrame().show())
            
        else:
            # Aquí podrías mostrar un mensaje de error
            print("Credenciales inválidas")
    
    def validate_credentials(self, usuario: str, password: str) -> bool:
        """
        Valida las credenciales del usuario
        Por ahora es un placeholder que acepta cualquier usuario no vacío
        """
        # TODO: Implementar validación real con base de datos
        return bool(usuario and password)


    def iniciar_servidor_udp(self):
        import multiprocessing
        import sys
        from pathlib import Path
        
        def run_udp_server():
            """Función que ejecuta el servidor"""
            backend_path = Path(__file__).parent.parent.parent / "backend" / "UDPserver"
            sys.path.insert(0, str(backend_path))
            
            from backend.UDPserver.server import run_server
            
            run_server()
    # Crear proceso independiente
        proceso = multiprocessing.Process(target=run_udp_server, daemon=True)
        proceso.start()
    
        print(f"✅ Servidor UDP iniciado en proceso separado (PID: {proceso.pid})")

def login():
    """Función de conveniencia para iniciar el frame"""
    LoginFrame().show()
