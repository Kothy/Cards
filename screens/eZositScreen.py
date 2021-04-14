import tkinter as tk
from Constants import *
from canvases.BarCanvas import BarCanvas
import copy


class eZositScreen:
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas
        self.canvas = tk.Canvas(self.parentCanvas, width=WWIDTH, height=WHEIGHT, bg="pink", takefocus=0,
                                highlightthickness=0)

        self.innerWindow = self.parentCanvas.create_window(0, 0, anchor=NW, window=self.canvas)
        self.createRightBar()
        barWidth = WWIDTH - DESKTOPWMAX
        self.iconH, self.iconW = barWidth - 30, barWidth - 10
        self.selectedTkId = None
        self.selectedFunction = None

    def createRightBar(self):
        barWidth = WWIDTH - DESKTOPWMAX
        self.rightBar = BarCanvas(self, self.canvas, WWIDTH - barWidth - 5, 0, PRIMARYCOLOR, barWidth, WHEIGHT)

        h, w = barWidth - 30, barWidth - 10
        x = 190
        space = 25
        dy = 5
        self.ys = []
        self.rightBar.addImage("images/buttons/eZositIcons/save.png", barWidth / 2,
                               10 + h / 2, w, h, SAVE, None, True, anchor=CENTER,
                               enterComm=lambda x: self.nothing(SAVE), leaveComm=lambda x: self.nothing(SAVE))
        self.rightBar.addImage("images/buttons/eZositIcons/new.png", barWidth / 2, (20 + h * 1) + space,
                               w, h, LOADULOHA, None, True, anchor=CENTER,enterComm=lambda x: self.nothing(LOADULOHA),
                               leaveComm=lambda x: self.nothing(LOADULOHA))

        self.rightBar.addStaticImage("images/buttons/separator.png", barWidth / 2, (h * 2) + space, barWidth - 10, 2)
        y = x + space
        self.ys.append(y)
        self.rightBar.addImage("images/buttons/eZositIcons/copy.png", barWidth / 2, x + space, w, h, COPY,
                               lambda x: self.selectIcon(COPY), True, anchor=CENTER,
                               enterComm=lambda x: self.nothing(COPY), leaveComm=lambda x: self.nothing(COPY))
        y = (x + (h + dy)) + space
        self.ys.append(y)
        self.rightBar.addImage("images/buttons/eZositIcons/paste.png", barWidth / 2, y, w, h,
                               PASTE, lambda x: self.selectIcon(PASTE), True, anchor=CENTER,
                               enterComm=lambda x: self.nothing(PASTE), leaveComm=lambda x: self.nothing(PASTE))

        y = (x + (h + dy) * 2) + space
        self.ys.append(y)
        self.rightBar.addImage("images/buttons/eZositIcons/remove.png", barWidth / 2, y,
                               w, h, REMOVEOBJECT, lambda x: self.selectIcon(REMOVEOBJECT), True,
                               anchor=CENTER, enterComm=lambda x: self.nothing(REMOVEOBJECT),
                               leaveComm=lambda x: self.nothing(REMOVEOBJECT))
        y = (x + (h + dy) * 3) + space
        self.ys.append(y)
        self.rightBar.addImage("images/buttons/eZositIcons/enlarge.png", barWidth / 2,
                               (x + (h + dy) * 3) + space, w, h, UPSIZE,
                               lambda x: self.selectIcon(UPSIZE), True, anchor=CENTER,
                               enterComm=lambda x: self.nothing(UPSIZE), leaveComm=lambda x: self.nothing(UPSIZE))

        y = (x + (h + dy) * 4) + space
        self.ys.append(y)
        self.rightBar.addImage("images/buttons/eZositIcons/shrink.png", barWidth / 2, y,
                               w, h, DOWNSIZE, lambda x: self.selectIcon(DOWNSIZE), True,
                               anchor=CENTER, enterComm=lambda x: self.nothing(DOWNSIZE),
                               leaveComm=lambda x: self.nothing(DOWNSIZE))

        y = (x + (h + dy) * 5) + space
        self.ys.append(y)
        self.rightBar.addImage("images/buttons/eZositIcons/vflip.png", barWidth / 2, y, w,
                               h, FLIPVERTICALLY, lambda x: self.selectIcon(FLIPVERTICALLY), True,
                               anchor=CENTER, enterComm=lambda x: self.nothing(FLIPVERTICALLY),
                               leaveComm=lambda x: self.nothing(FLIPVERTICALLY))

        y = (x + (h + dy) * 6) + space
        self.ys.append(y)
        self.rightBar.addImage("images/buttons/eZositIcons/hflip.png", barWidth / 2, y, w,
                               h, FLIPHORIZONTALLY, lambda x: self.selectIcon(FLIPHORIZONTALLY), True,
                               anchor=CENTER, enterComm=lambda x: self.nothing(FLIPHORIZONTALLY),
                               leaveComm=lambda x: self.nothing(FLIPHORIZONTALLY))


    def nothing(self, text):
        print(text)

    def getY(self, text):
        if text == COPY:
            return self.ys[0]
        elif text == PASTE:
            return self.ys[1]
        elif text == REMOVEOBJECT:
            return self.ys[2]
        elif text == UPSIZE:
            return self.ys[3]
        elif text == DOWNSIZE:
            return self.ys[4]
        elif text == FLIPVERTICALLY:
            return self.ys[5]
        elif text == FLIPHORIZONTALLY:
            return self.ys[6]

    def selectIcon(self, text):
        x = (WWIDTH - DESKTOPWMAX)/2
        y = self.getY(text)
        if self.selectedTkId is not None:
            self.rightBar.canvas.delete(self.selectedTkId)

        if self.selectedFunction != text:
            self.selectedFunction = None
            self.selectedTkId = 0
            self.selectedFunction = text
            self.selectedTkId = self.createRectangle(self.rightBar.canvas, x, y, self.iconW - 20, self.iconH)
        else:
            self.selectedFunction = None
            self.selectedTkId = 0

    def createRectangle(self, canvas, x, y, w, h, color="grey"):
        return canvas.create_rectangle(x - (w / 2), y - (h / 2), x + (w / 2), y + (h / 2), outline=color, width=2)
