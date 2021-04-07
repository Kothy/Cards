import tkinter as tk
from Constants import *
import tkinter.ttk as ttk

WW = 450
WH = 500


class CheckboxCanvas:
    def __init__(self, parent, parentCanvas, command):
        self.parentCanvas = parentCanvas
        self.parent = parent
        x, y = WWIDTH, WHEIGHT
        self.canvas = tk.Canvas(self.parentCanvas, bg="white", width=WW, height=WH, highlightthickness=0)
        self.window = self.parentCanvas.create_window(x / 2, y / 2, anchor="c", window=self.canvas, width=WW, height=WH)
        self.createCheckboxes(command)
        self.hide()

    def createCheckboxes(self, command):
        fon = tk.font.Font()
        fon.configure()
        fon.configure(weight="bold")
        fon.configure(size=22)
        fon.configure(family=FONT)

        self.lab = ttk.Label(self.canvas, text=TOOLS, font=fon, background=WHITE)
        self.lab.place(relx=0.5, rely=0.10, anchor="c")

        checks = [UPSIZE, DOWNSIZE, FLIPHORIZONTALLY, FLIPVERTICALLY, COPYPASTE, REMOVEOBJECT]
        self.checkbuttons = []

        style = ttk.Style()
        style.configure("MyK.TCheckbutton", font=(FONT, 18), anchor="w", background=WHITE)

        rely = 0.22
        for i in range(len(checks)):
            checkVar = tk.IntVar()
            check = ttk.Checkbutton(self.canvas, text=checks[i], variable=checkVar, onvalue=i + 1, style="MyK.TCheckbutton",
                                    width=len(checks[i]), takefocus=False)
            check.place(relx=0.08, rely=rely, anchor="w")
            self.checkbuttons.append([check, checkVar, checks[i]])
            rely += 0.09

        style2 = ttk.Style()
        style2.configure('Submit.TButton', font=(FONT, 20), justify=tk.TOP)
        self.button = ttk.Button(self.canvas, text=SET, command=command, style='Submit.TButton')
        self.button.place(relx=0.5, rely=0.88, anchor="c")

    def hide(self):
        self.parentCanvas.itemconfig(self.window, state="hidden")

    def show(self):
        self.parentCanvas.itemconfig(self.window, state="normal")
