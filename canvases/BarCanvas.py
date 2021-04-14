import tkinter as tk
from PIL import ImageTk, Image
from CommonFunctions import resize_image
from Constants import *
import tkinter.ttk as ttk


class BarCanvas:
    def __init__(self, parent, parentCanvas, x, y, bgCol, w, h):
        self.parent = parent
        self.parentCanvas = parentCanvas
        self.width = w
        self.height = h
        self.x, self.y = x, y
        self.bgCol = bgCol
        self.canvas = tk.Canvas(self.parentCanvas, width=w, height=h, bg=bgCol, highlightthickness=2)
        self.window = self.parentCanvas.create_window(x, y, anchor="nw", window=self.canvas)
        self.images = []
        self.texts = []
        self.scales = []
        self.labels = []
        self.buttons = []

    def addImage(self, path, x, y, w, h, altText, command, ratioResize=False, anchor="nw", text=False, rel=False, enterComm=None, leaveComm=None):
        img = Image.open(path)
        if ratioResize:
            img = resize_image(img, w, h)
        else:
            img = img.resize((w, h))
        imgObj = ImageTk.PhotoImage(img)
        if not rel:
            id = self.canvas.create_image(x, y, image=imgObj, anchor=anchor)
        else:
            id = self.canvas.create_image(self.width * x, self.height * y, image=imgObj, anchor=anchor)

        textId = 0
        if text and not rel:
            textId = self.canvas.create_text(x - 3, y - 3, text=altText)
        elif text and rel:
            textId = self.canvas.create_text((self.width * x) - 3, (self.height * y) - 3, text=altText)

        if text:
            self.canvas.tag_bind(textId, "<Button-1>", command)
            self.canvas.tag_bind(textId, "<Enter>", lambda e: self.displayInfo(i))
            self.canvas.tag_bind(textId, "<Leave>", self.hideInfo)

        self.images.append((img, imgObj, id, altText, x, y, textId))
        i = len(self.images) - 1
        leaveCommand = self.hideInfo if leaveComm is None else leaveComm
        enterCommand = (lambda e: self.displayInfo(i)) if enterComm is None else enterComm
        # self.canvas.tag_bind(id, "<Enter>", lambda e: self.displayInfo(i))
        # self.canvas.tag_bind(id, "<Leave>", self.hideInfo)
        self.canvas.tag_bind(id, "<Enter>", enterCommand)
        self.canvas.tag_bind(id, "<Leave>", leaveCommand)
        self.canvas.tag_bind(id, "<Button-1>", command)
        return id

    def addStaticImage(self, path, x, y, w, h):
        img = Image.open(path)
        img = img.resize((w, h))
        imgObj = ImageTk.PhotoImage(img)
        id = self.canvas.create_image(x, y, image=imgObj, anchor=CENTER)
        self.images.append((img, imgObj, id, "", x, y, 0))

    def removeImage(self, tkId):
        for i in range(len(self.images)):
            (img, imgObj, id, altText, x, y, textId) = self.images[i]
            if id == tkId:
                self.canvas.delete(id)
                self.images.pop()
                break

    def removeAllImages(self):
        i = 0
        while len(self.images) > 0:
            (img, imgObj, id, altText, x, y, textId) = self.images[i]
            self.canvas.delete(id)
            self.images.pop()

    def displayInfo(self, i):
        self.parent.changeInfoLabelText(OBJECTINFO.format(self.images[i][3]))

    def hideInfo(self, _):
        self.parent.changeInfoLabelText(OBJECTINFOEMPTY)

    def addScale(self, name, var, startValue, command, from_, to, xrel, yrel, addToList=True, cursor="arrow", length=200):
        var.set(startValue)
        s = ttk.Style()
        s.configure('Horizontal.TScale', background=PRIMARYCOLOR, activebackground=SECONDARYCOLOR)
        scale = ttk.Scale(self.canvas, command=command, variable=var, from_=from_, to=to,
                          orient=tk.HORIZONTAL, length=length, cursor=cursor, style="Horizontal.TScale")

        scale.place(relx=xrel, rely=yrel, anchor="w", )
        if addToList:
            self.scales.append((name, scale, xrel, yrel))
        return scale

    def addLabel(self, text, bg, relx, rely):
        label = tk.Label(self.canvas, text=text, bg=bg, height=2)
        label.place(relx=relx, rely=rely, anchor='w')
        self.labels.append((label, text, bg, relx, rely))
        return label

    def addButton(self, text, command, relx, rely):
        button = tk.Button(self.canvas, text=text, command=command)
        button.place(relx=relx, rely=rely, anchor='w')
        self.buttons.append((button, text, command, relx, rely))
        return button

    def hide(self):
        self.parentCanvas.itemconfig(self.window, state="hidden")

    def show(self):
        self.parentCanvas.itemconfig(self.window, state="normal")

    def lower(self):
        self.parent.getCanvas().tag_lower(self.window)