#!/usr/bin/python
from tkinter import *
from tkinter import ttk

class Juniemobile(Tk):

    def __init__(self):
        super().__init__()
        self.wm_title("Juniemobile")
        self.geometry("600x400")
        self.configure(bg="#0f1419")


if __name__ == "__main__":
    app = Juniemobile()
    app.mainloop()