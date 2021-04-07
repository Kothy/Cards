import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from Constants import *
from CommonFunctions import resize_image

wMax = 100
hMax = 100
BUTTONH = 30
BUTTONW = wMax / 2
ICOARROWR = "images/buttons/rightGrey.png"
ICOARROWL = "images/buttons/leftGrey.png"


class ClickableChangeOrderImagesScreen:
    def __init__(self, parent, w, h):
        self.parent = parent
        self.parentWidth = w
        self.parentHeight = h
        self.width = self.parentWidth / 1.5
        self.height = self.parentHeight / 1.5
        self.command = None
        self.transImg = Image.open(IMAGETRANSPARENT)
        self.transImg = self.transImg.resize((self.parent.windowWidth, self.parent.windowHeight))
        self.transImgObj = ImageTk.PhotoImage(self.transImg)
        self.transBgTkId = 0
        self.object = None
        self.objects = []
        img = resize_image(Image.open(ICOARROWR), BUTTONW - 5, BUTTONH - 13)
        self.nextButtonImage = ImageTk.PhotoImage(img)
        img = resize_image(Image.open(ICOARROWL), BUTTONW - 5, BUTTONH - 13)
        self.prevButtonImage = ImageTk.PhotoImage(img)

    def show(self):
        pw, ph = self.parentWidth, self.parentHeight
        w, h = self.width, self.height
        self.transBgTkId = self.parent.getCanvas().create_image(0, 0, image=self.transImgObj, anchor='nw')
        self.canvas = tk.Canvas(self.parent.getCanvas(), width=w, height=h, highlightthickness=0, bg=WHITE)
        self.window = self.parent.getCanvas().create_window(pw / 2, ph / 2, anchor="c", window=self.canvas, width=w,
                                                            height=h)

    def setCommand(self, command):
        self.command = command

    def hide(self):
        self.parent.getCanvas().itemconfig(self.window, state="hidden")
        self.parent.getCanvas().delete(self.transBgTkId)
        self.objects = []
        self.object = None

    def showImages(self, obj):
        self.object = obj
        self.style = ttk.Style()
        self.style.configure('Submit.TButton', font=(FONT, 20), justify=tk.TOP)
        self.submitButton = ttk.Button(self.canvas, text=SUBMIT, command=self.submit, style="Submit.TButton")
        self.submitButton.place(relx=0.5, rely=0.9, anchor='c')

        padX, padX2, padY, padY2 = 20, 30, 80, 40
        xStart = ((wMax / 2) + padX) + padX2
        yStart = (hMax / 2) + padY2
        x, y = xStart, yStart
        dx, dy = wMax + padX, hMax + padY
        self.movableImages = []
        i = 0

        for image in obj.images:
            selected = True if obj.index == i else False

            if x + dx > (self.width + 20):
                x = xStart
                y += dy

            self.movableImages.append(MovableImage(self, x, y, image, i, selected))
            x += dx
            i += 1

    def submit(self):
        images = []
        index = 0
        for movImage in self.movableImages:
            if movImage.selected:
                index = movImage.index

            images.append(movImage.imgOrigin)

        self.object.changeIndex(index)
        self.object.changeImages3(images)
        self.command()


class MovableImage:
    def __init__(self, parent, x, y, image, index, selected):
        self.parent = parent
        self.canvas = parent.canvas
        self.index = index
        self.imgOrigin = image
        self.image = resize_image(image, wMax, hMax)
        self.imgObj = ImageTk.PhotoImage(self.image)
        self.width, self.height = self.image.size
        self.movImages = parent.movableImages
        self.x, self.y = x, y
        self.tkId = 0
        self.borderTkId = 0
        self.prevButton = None
        self.nextButton = None
        self.style = ttk.Style()
        self.style.configure('Klaudia.TButton', font=(FONT, 15), justify=tk.TOP)
        self.selected = selected
        self.draw()

    def drawBorder(self):
        x, y = self.x, self.y
        self.borderTkId = self.canvas.create_rectangle(x - (wMax / 2) - 4, y - (hMax / 2) - 4, x + (wMax / 2) + 4,
                                                       y + (hMax / 2) + 4, outline="grey", width=2)

    def draw(self):
        x, y = self.x, self.y
        next, prev = self.parent.nextButtonImage, self.parent.prevButtonImage
        w, h = self.width, self.height

        self.canvas.delete(self.tkId)
        self.canvas.delete(self.borderTkId)
        if self.prevButton is not None:
            self.prevButton.destroy()

        if self.nextButton is not None:
            self.nextButton.destroy()

        self.tkId = self.canvas.create_image(x, y, image=self.imgObj, anchor='c')
        self.canvas.tag_bind(self.tkId, "<Button-1>", self.select)
        self.prevButton = ttk.Button(self.canvas, command=self.moveLeft, style="Klaudia.TButton",
                                     image=prev)
        self.prevButton.place(x=x - (wMax / 2), y=y + (hMax / 2) + 5, anchor='nw', width=BUTTONW, height=BUTTONH)
        self.nextButton = ttk.Button(self.canvas, command=self.moveRight, style="Klaudia.TButton",
                                     image=next)
        self.nextButton.place(x=x - (wMax / 2) + (wMax / 2), y=y + (hMax / 2) + 5, anchor='nw', width=BUTTONW, height=BUTTONH)
        if self.selected:
            self.drawBorder()

    def moveRight(self):
        if self.index + 1 < len(self.movImages):
            self.changePos(self.movImages[self.index + 1])

    def moveLeft(self):
        if self.index - 1 >= 0:
            self.changePos(self.movImages[self.index - 1])

    def changePos(self, other):
        self.x, self.y, other.x, other.y = other.x, other.y, self.x, self.y
        self.movImages[self.index], self.movImages[other.index] = self.movImages[other.index], self.movImages[
            self.index]
        self.index, other.index = other.index, self.index

        self.draw()
        other.draw()

    def select(self, _):
        for movImg in self.movImages:
            movImg.unselect()

        self.selected = True
        self.drawBorder()

    def unselect(self):
        self.selected = False
        self.canvas.delete(self.borderTkId)
