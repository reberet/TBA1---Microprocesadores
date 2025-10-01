

def inicio():
    from frames.gui_login import login
    from pathlib import Path
    from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    window = Tk()

    window.geometry("1440x1024")
    window.configure(bg = "#153573")


    canvas = Canvas(
        window,
        bg = "#153573",
        height = 1024,
        width = 1440,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        720.0,
        512.0,
        image=image_image_1
    )

    iniciarImagen = PhotoImage(
        file=relative_to_assets("button_1.png"))
    iniciar = Button(
        image=iniciarImagen,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), login()],
        relief="flat"
    )
    iniciar.place(
        x=138.0,
        y=633.0,
        width=197.0,
        height=38.0
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        1185.0,
        63.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        1340.0,
        68.0,
        image=image_image_3
    )

    canvas.create_text(
        138.0,
        388.0,
        anchor="nw",
        text="MANTEL DATACENTER’S",
        fill="#FFFFFF",
        font=("Arial BoldMT", 96 * -1)
    )

    canvas.create_text(
        138.0,
        512.0,
        anchor="nw",
        text="Un ecosistema de soluciones digitales para \nimpulsar el desarrollo de tu negocio",
        fill="#FFFFFF",
        font=("ArialMT", 32 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

    
