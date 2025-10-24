"""
Configurar Datos Frame - Gestión completa de datos (ver, editar, eliminar)
"""
from tkinter import Button, Toplevel, Entry, StringVar, OptionMenu, Label
from frames.base_frame import BaseFrame
from components.sidebar import Sidebar
from models import dato_manager, TipoDato, EstadoBinario
from utils.navigation import nav

class ConfigurarDatosFrame(BaseFrame):
    """Frame para configurar datos (listar, editar, eliminar, y botón para agregar)"""
    
    def __init__(self):
        super().__init__(bg_color="#B1CCFF")
        self.frame_name = "frame3"
        self.sidebar = None
    
    def build(self):
        """Construye la UI del frame de configuración"""
        user_data = nav.get_user_data()
        username = user_data.get('username', 'Nombre Apellido')
        
        # Crear sidebar
        self.sidebar = Sidebar(self.canvas, self.image_manager, 
                              self.frame_name, username)
        self.sidebar.create(
            on_dashboard=self.go_to_dashboard,
            on_datos=self.go_to_datos,
            on_alarmas=self.go_to_alarmas,
            on_configurar=self.refresh,
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
            text="Configurar Datos",
            fill="#FFFFFF",
            font=("Arial BoldMT", 32)
        )
        
        # Lista de datos existentes con opciones de editar/eliminar
        self.create_datos_list()
    
    def create_datos_list(self):
        """Crea la lista de datos existentes con botones de acción"""
        list_start_y = 140.0
        row_height = 60.0
        
        # Headers
        self.canvas.create_rectangle(
            414.0, list_start_y, 1337.0, list_start_y + 40.0,
            fill="#142D5D",
            outline=""
        )
        
        self.canvas.create_text(
            432.0, list_start_y + 10.0,
            anchor="nw",
            text="Nombre",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            650.0, list_start_y + 10.0,
            anchor="nw",
            text="Tipo",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            800.0, list_start_y + 10.0,
            anchor="nw",
            text="Valor Actual",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            980.0, list_start_y + 10.0,
            anchor="nw",
            text="Rango/Estado",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        self.canvas.create_text(
            1200.0, list_start_y + 10.0,
            anchor="nw",
            text="Acciones",
            fill="#FFFFFF",
            font=("ArialMT", 20)
        )
        
        # Obtener datos
        datos = dato_manager.get_datos_activos()
        data_start_y = list_start_y + 50.0
        
        if not datos:
            self.canvas.create_text(
                883.0, 400.0,
                text="No hay datos configurados\nPresiona '+ Agregar Nuevo Dato' para comenzar",
                fill="#FFFFFF",
                font=("ArialMT", 20),
                anchor="center",
                justify="center"
            )
        else:
            # Renderizar cada dato
            for i, dato in enumerate(datos):
                y_pos = data_start_y + (i * row_height)
                
                # Fondo de fila (alternado)
                fill_color = "#152D5D" if i % 2 == 0 else "#1a3568"
                self.canvas.create_rectangle(
                    414.0, y_pos, 1337.0, y_pos + 50.0,
                    fill=fill_color,
                    outline=""
                )
                
                # Nombre
                self.canvas.create_text(
                    432.0, y_pos + 15.0,
                    anchor="nw",
                    text=dato.nombre,
                    fill="#FFFFFF",
                    font=("ArialMT", 16)
                )
                
                # Tipo
                tipo_texto = "Rango" if dato.tipo == TipoDato.RANGO else "Binario"
                self.canvas.create_text(
                    650.0, y_pos + 15.0,
                    anchor="nw",
                    text=tipo_texto,
                    fill="#FFFFFF",
                    font=("ArialMT", 16)
                )
                
                # Valor actual
                self.canvas.create_text(
                    800.0, y_pos + 15.0,
                    anchor="nw",
                    text=dato.get_valor_formateado(),
                    fill="#FFFFFF",
                    font=("ArialMT", 16)
                )
                
                # Rango o Estado esperado
                if dato.tipo == TipoDato.RANGO and dato.alarma:
                    rango_texto = f"{dato.alarma.valor_minimo}-{dato.alarma.valor_maximo}{dato.unidad}"
                elif dato.tipo == TipoDato.BINARIO and dato.alarma:
                    rango_texto = f"Esp: {dato.alarma.estado_esperado.value}"
                else:
                    rango_texto = "Sin alarma"
                
                self.canvas.create_text(
                    980.0, y_pos + 15.0,
                    anchor="nw",
                    text=rango_texto,
                    fill="#FFFFFF",
                    font=("ArialMT", 16)
                )
                
                # Botón Eliminar
                btn_eliminar = Button(
                    text="🗑️",
                    bg="#FF4444",
                    fg="#FFFFFF",
                    font=("ArialMT", 18),
                    borderwidth=0,
                    command=lambda n=dato.nombre: self.eliminar_dato(n),
                    cursor="hand2",
                    width=3
                )
                btn_eliminar.place(x=1240.0, y=y_pos + 8, width=40, height=35)
        
        # Calcular posición para el botón de agregar (después de la lista)
        num_datos = len(datos)
        button_y = data_start_y + (num_datos * row_height) + 30.0
        
        # Botón "Agregar Nuevo Dato" (grande y destacado)
        btn_agregar = Button(
            text="+ Agregar Nuevo Dato",
            bg="#F8BC04",
            fg="#000000",
            font=("Arial BoldMT", 20),
            borderwidth=0,
            command=self.abrir_formulario_agregar,
            cursor="hand2",
            relief="flat",
            activebackground="#e0a804"
        )
        btn_agregar.place(x=550.0, y=button_y, width=350, height=50)
    
    def abrir_formulario_agregar(self):
        """Abre una ventana modal para agregar un nuevo dato"""
        # Crear ventana modal
        modal = Toplevel(self.window)
        modal.title("Agregar Nuevo Dato")
        modal.geometry("600x550")
        modal.configure(bg="#153573")
        modal.resizable(False, False)
        modal.transient(self.window)
        modal.grab_set()
        
        # Título
        Label(
            modal,
            text="Crear Nuevo Dato",
            bg="#153573",
            fg="#FFFFFF",
            font=("Arial BoldMT", 24)
        ).pack(pady=20)
        
        # Frame para el formulario
        form_frame = Label(modal, bg="#153573")
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        entries = {}
        
        # Nombre
        self._create_form_field(form_frame, "Nombre:", entries, "nombre", row=0)
        
        # Tipo (con dropdown)
        Label(form_frame, text="Tipo:", bg="#153573", fg="#FFFFFF", 
              font=("ArialMT", 16)).grid(row=1, column=0, sticky="w", pady=10)
        tipo_var = StringVar(modal)
        tipo_var.set("Rango")
        tipo_menu = OptionMenu(modal, tipo_var, "Rango", "Binario")
        tipo_menu.config(bg="#D9D9D9", font=("ArialMT", 14), width=30)
        tipo_menu.grid(in_=form_frame, row=1, column=1, pady=10)
        entries['tipo'] = tipo_var
        
        # Valor Inicial
        self._create_form_field(form_frame, "Valor Inicial:", entries, "valor", row=2)
        
        # Unidad
        self._create_form_field(form_frame, "Unidad (ej: °C, %):", entries, "unidad", row=3)
        
        # Valor Mínimo
        self._create_form_field(form_frame, "Valor Mínimo:", entries, "min", row=4)
        
        # Valor Máximo
        self._create_form_field(form_frame, "Valor Máximo:", entries, "max", row=5)
        
        # Importancia
        Label(form_frame, text="Importancia:", bg="#153573", fg="#FFFFFF", 
              font=("ArialMT", 16)).grid(row=6, column=0, sticky="w", pady=10)
        importancia_var = StringVar(modal)
        importancia_var.set("Normal")
        importancia_menu = OptionMenu(modal, importancia_var, "Normal", "Importante", "Crítico")
        importancia_menu.config(bg="#D9D9D9", font=("ArialMT", 14), width=30)
        importancia_menu.grid(in_=form_frame, row=6, column=1, pady=10)
        entries['importancia'] = importancia_var
        
        # Botones
        btn_frame = Label(modal, bg="#153573")
        btn_frame.pack(pady=20)
        
        Button(
            btn_frame,
            text="Cancelar",
            bg="#666666",
            fg="#FFFFFF",
            font=("ArialMT", 14),
            command=modal.destroy,
            cursor="hand2",
            width=12
        ).pack(side="left", padx=10)
        
        Button(
            btn_frame,
            text="Guardar",
            bg="#44FF44",
            fg="#000000",
            font=("Arial BoldMT", 14),
            command=lambda: self.guardar_dato(entries, modal),
            cursor="hand2",
            width=12
        ).pack(side="left", padx=10)
    
    def _create_form_field(self, parent, label_text, entries_dict, key, row):
        """Helper para crear un campo del formulario"""
        Label(
            parent,
            text=label_text,
            bg="#153573",
            fg="#FFFFFF",
            font=("ArialMT", 16)
        ).grid(row=row, column=0, sticky="w", pady=10)
        
        entry = Entry(
            parent,
            bg="#D9D9D9",
            fg="#000716",
            font=("ArialMT", 14),
            width=35
        )
        entry.grid(row=row, column=1, pady=10)
        entries_dict[key] = entry
    
    def guardar_dato(self, entries, modal):
        """Guarda el nuevo dato"""
        nombre = entries['nombre'].get().strip()
        tipo_str = entries['tipo'].get()
        valor_str = entries['valor'].get().strip()
        importancia = entries['importancia'].get()
        
        if not nombre or not valor_str:
            print("Error: Nombre y valor son requeridos")
            return
        
        try:
            if tipo_str == "Rango":
                valor = float(valor_str)
                unidad = entries['unidad'].get().strip()
                valor_min_str = entries['min'].get().strip()
                valor_max_str = entries['max'].get().strip()
                
                if not valor_min_str or not valor_max_str:
                    print("Error: Valores mínimo y máximo son requeridos para tipo Rango")
                    return
                
                valor_min = float(valor_min_str)
                valor_max = float(valor_max_str)
                
                dato_manager.crear_dato_rango(
                    nombre=nombre,
                    valor_inicial=valor,
                    unidad=unidad,
                    valor_min=valor_min,
                    valor_max=valor_max,
                    importancia=importancia
                )
            else:  # Binario
                estado = EstadoBinario.BIEN if valor_str.lower() in ['bien', 'ok', '1', 'true'] else EstadoBinario.MAL
                dato_manager.crear_dato_binario(
                    nombre=nombre,
                    valor_inicial=estado,
                    estado_esperado=EstadoBinario.BIEN,
                    importancia=importancia
                )
            
            print(f"✓ Dato '{nombre}' creado correctamente")
            modal.destroy()
            # Recargar el frame
            nav.navigate_to(lambda: ConfigurarDatosFrame().show())
            
        except ValueError as e:
            print(f"Error: Valores numéricos inválidos - {e}")
        except Exception as e:
            print(f"Error al crear dato: {e}")
    
    def eliminar_dato(self, nombre: str):
        """Elimina un dato del sistema"""
        if dato_manager.eliminar_dato(nombre):
            print(f"✓ Dato '{nombre}' eliminado")
            nav.navigate_to(lambda: ConfigurarDatosFrame().show())
        else:
            print(f"✗ Error al eliminar '{nombre}'")
    
    def refresh(self):
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

def configurar_datos():
    """Función de conveniencia para iniciar el frame"""
    ConfigurarDatosFrame().show()
