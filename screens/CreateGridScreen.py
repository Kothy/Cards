from Constants import *
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.ttk as ttk
from tkcolorpicker import askcolor


class CreateGridScreen:
    def __init__(self, parent, w, h, command):
        self.parent = parent
        self.command = command
        self.parentWidth = w
        self.parentHeight = h
        self.width = self.parentWidth / 2.5
        self.height = self.parentHeight / 2.5
        self.transImg = Image.open(IMAGETRANSPARENT)
        self.transImg = self.transImg.resize((self.parent.windowWidth, self.parent.windowHeight))
        self.transImgObj = ImageTk.PhotoImage(self.transImg)
        self.transBgTkId = 0
        pw, ph = self.parentWidth, self.parentHeight
        w, h = self.width, self.height
        self.parent.getCanvas().tkraise(self.transBgTkId)
        self.canvas = tk.Canvas(self.parent.getCanvas(), width=w, height=h, highlightthickness=0, bg=WHITE)
        self.window = self.parent.getCanvas().create_window(pw / 2, ph / 2, anchor=CENTER, window=self.canvas, width=w,
                                                            height=h)
        self.style = ttk.Style()
        self.style.configure(SUBMITSTYLE, font=(FONT, 20), justify=tk.TOP, highlightthickness=0)
        self.submitButton = ttk.Button(self.canvas, text=SUBMIT, command=lambda: self.command(self, True),
                                       style=SUBMITSTYLE, takefocus=False)
        self.submitButton.place(relx=0.35, rely=0.9, anchor=CENTER)

        self.cancelButton = ttk.Button(self.canvas, text=CANCEL, command=lambda: self.command(self, False),
                                       style=SUBMITSTYLE, takefocus=False)
        self.cancelButton.place(relx=0.65, rely=0.9, anchor=CENTER)

        self.rowsNum = tk.StringVar()
        self.colsNum = tk.StringVar()
        self.rowsNum.set("1")
        self.colsNum.set("1")
        self.rows = ttk.Spinbox(self.canvas, from_=1, to=10, width=5, textvariable=self.rowsNum,
                                style=SPINSTYLE, font=(FONT, 20))

        self.cols = ttk.Spinbox(self.canvas, from_=1, to=10, width=5, textvariable=self.colsNum,
                                style=SPINSTYLE, font=(FONT, 20))

        self.rowsLabel = ttk.Label(self.canvas, text=ROWNUM, font=(FONT, 18))
        self.colsLabel = ttk.Label(self.canvas, text=COLNUM, font=(FONT, 18))
        self.colorLabel = ttk.Label(self.canvas, text=GRIDCOLOR, font=(FONT, 18))
        self.colorTkId = self.createRectangle(self.canvas, 255, 263, 40, 40, BLACK)
        self.canvas.itemconfig(self.colorTkId, fill=BLACK)
        self.canvas.tag_bind(self.colorTkId, BINDLEFTBUTT, self.chooseColor)
        self.color = (BLACK, BLACK)
        style = ttk.Style()
        style.configure(MYKCHECKSTYLE, font=(FONT, 20), anchor=W, background=WHITE)
        self.gridLineVar = tk.BooleanVar()
        self.gridLineVar.set(True)
        self.gridLineCheck = ttk.Checkbutton(self.canvas, text=GRIDLINE, variable=self.gridLineVar, onvalue=True,
                                             style=MYKCHECKSTYLE, width=50, takefocus=False)

        relX1 = 0.28
        relX2 = 0.03
        relY1 = 0.15
        relY2 = 0.3
        relY3 = 0.45
        relY4 = 0.6
        self.rows.place(relx=relX1, rely=relY1)
        self.cols.place(relx=relX1, rely=relY2)
        self.rowsLabel.place(relx=relX2, rely=relY1)
        self.colsLabel.place(relx=relX2, rely=relY2)
        self.gridLineCheck.place(relx=0.025, rely=relY3)
        self.colorLabel.place(relx=relX2, rely=relY4)
        self.object = None
        self.hide()

    def chooseColor(self, _):
        color = askcolor(self.color[1])
        if color is not None and color != (None, None):
            self.canvas.itemconfig(self.colorTkId, fill=color[1])
            self.color = color

    def show(self):
        self.transBgTkId = self.parent.getCanvas().create_image(0, 0, image=self.transImgObj, anchor=NW)
        self.parent.getCanvas().itemconfig(self.window, state=NORMAL)

    def hide(self):
        self.parent.getCanvas().itemconfig(self.window, state=HIDDEN)
        self.parent.getCanvas().delete(self.transBgTkId)

    def createGridFromObject(self):
        x, y = self.object.x, self.object.y
        startX, startY = self.object.x, self.object.y

        rows = int(self.rowsNum.get())
        cols = int(self.colsNum.get())
        spaces = 10
        gridW, gridH = self.object.width + spaces, self.object.height + spaces
        for i in range(rows):
            for j in range(cols):
                self.object.copy(x, y)
                if self.gridLineVar.get():
                    color = None
                    if type(self.color) == tuple:
                        color = self.color[1]
                    else:
                        color = self.color
                    self.parent.desktopCanvas.addGrid(x, y, gridW, gridH, color)
                x += self.object.width + spaces

            y += self.object.height + spaces
            x = startX

        self.object.remove()
        self.object = None
        self.parent.removeItemScales()

    def createRectangle(self, canvas, x, y, w, h, color):
        return canvas.create_rectangle(x - (w / 2), y - (h / 2), x + (w / 2), y + (h / 2), outline=color, width=2)
