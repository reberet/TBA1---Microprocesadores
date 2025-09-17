from frames.gui_inicio import inicio
from pathlib import Path
from tkinter import *


def main ():
    window = Tk()

    window.geometry("1440x1024")
    window.configure(bg = "#153573")

    inicio(window)
    window.resizable(False, False)
    window.mainloop()
main()
