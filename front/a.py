import tkinter as tk
from tkinter import font as tkfont

class Dashboard(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title("Dashboard")
        self.geometry("1000x600")

        # Contenedor principal para toda la aplicación
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Marco del menú lateral (similar a la imagen)
        sidebar_frame = tk.Frame(container, bg="#1a237e", width=200)
        sidebar_frame.pack(side="left", fill="y")
        
        # Etiqueta de usuario en la barra lateral
        user_label = tk.Label(sidebar_frame, text="JOHN DON", bg="#1a237e", fg="white", font=("Arial", 14, "bold"))
        user_label.pack(pady=20, padx=10, anchor="w")

        # Marco de las páginas (donde se mostrarán las diferentes secciones)
        self.frames = {}
        content_frame = tk.Frame(container)
        content_frame.pack(side="right", fill="both", expand=True)

        # Crear los marcos (páginas) y apilarlos
        for F in (HomePage, FilePage, MessagesPage):
            page_name = F.__name__
            frame = F(parent=content_frame, controller=self)
            self.frames[page_name] = frame
            # Coloca todos los marcos en la misma posición
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        # Botones de navegación en la barra lateral
        home_button = tk.Button(sidebar_frame, text="Home", command=lambda: self.show_frame("HomePage"))
        home_button.pack(fill="x", pady=5)
        
        file_button = tk.Button(sidebar_frame, text="File", command=lambda: self.show_frame("FilePage"))
        file_button.pack(fill="x", pady=5)
        
        messages_button = tk.Button(sidebar_frame, text="Messages", command=lambda: self.show_frame("MessagesPage"))
        messages_button.pack(fill="x", pady=5)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # Trae el marco seleccionado al frente

# --- Definición de las páginas (frames) ---

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Página de Inicio (Home)", font=controller.title_font)
        label.pack(pady=10, padx=10)
        
        # Puedes añadir más widgets para replicar el contenido de la imagen
        # Por ejemplo, los cuadros de "Earning", "Share", etc.

class FilePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Página de Archivos (File)", font=controller.title_font)
        label.pack(pady=10, padx=10)

class MessagesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Página de Mensajes (Messages)", font=controller.title_font)
        label.pack(pady=10, padx=10)

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
