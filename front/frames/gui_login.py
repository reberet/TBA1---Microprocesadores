

def login():

    from pathlib import Path
    
    from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame1")


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
        1080.0,
        512.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        354.0,
        248.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        145.0,
        922.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        554.0,
        921.0,
        image=image_image_4
    )

    canvas.create_text(
        42.0,
        541.0,
        anchor="nw",
        text="Contraseña",
        fill="#FFFFFF",
        font=("Arial BoldMT", 32 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        354.5,
        611.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=57.0,
        y=591.0,
        width=595.0,
        height=38.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        354.5,
        468.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=57.0,
        y=448.0,
        width=595.0,
        height=38.0
    )

    canvas.create_text(
        42.0,
        397.0,
        anchor="nw",
        text="Usuario",
        fill="#FFFFFF",
        font=("Arial BoldMT", 32 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=256.0,
        y=696.0,
        width=197.0,
        height=38.0
    )
    window.resizable(False, False)
    window.mainloop()
