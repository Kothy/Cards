from tkinter.filedialog import askopenfilenames
from PIL import ImageTk, Image
import tkinter as tk
import os
import copy
from serializeImg import imageToText
from Constants import *
from tkinter import messagebox


class ClickableObject:
    def __init__(self, parent, images, x, y, typ):  # draggable and static
        self.parent = parent
        self.index = 0

        self.imgObjs = []
        self.images = []
        self.imagesOrig = images
        sizeImage = images[0]
        w, h = sizeImage.size

        for iimage in images:
            i = iimage.resize((w, h))
            self.images.append(i)
            self.imgObjs.append(ImageTk.PhotoImage(i))

        self.type = typ
        self.x = x
        self.y = y
        self.renderedX = self.x
        self.renderedY = self.y
        self.width, self.height = self.images[self.index].size
        self.tkSelectId = 0
        self.tkId = 0
        self.createMenu()
        self.draw()
        self.setBinds()
        self.render()

    def draw(self):
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)
        self.tkId = self.createImage()
        if self.parent.selected:
            self.drawSelectBorder()
        self.setBinds()

    def createImage(self):
        return self.getCanvas().create_image(self.x, self.y, image=self.imgObjs[self.index], anchor='c')

    def copy(self, x=None, y=None):
        newX = self.x + 30 if x is None else x
        newY = self.y + 30 if y is None else y
        newObject = self.parent.parent.addObjectWithImages(self.images, self.type, newX, newY)
        newObject = newObject.getObject()
        newObject.typ = copy.copy(self.type)
        newObject.changeWidth(copy.copy(self.width), False)
        newObject.changeHeight(copy.copy(self.height), False)
        newObject.draw()

    def rotate(self, deg=90):
        self.width, self.height = self.height, self.width
        for i in range(len(self.images)):
            self.images[i] = self.images[i].rotate(deg, expand=True)
            self.imgObjs[i] = ImageTk.PhotoImage(self.images[i])

        if self.parent.selected:
            self.drawSelectBorder()
        self.draw()

    def setBinds(self):
        self.getCanvas().tag_bind(self.tkId, BINDRIGHTMOTION, self.onDrag)
        self.getCanvas().tag_bind(self.tkId, BINDDOUBLELEFT, self.onDoubleClick)
        self.getCanvas().tag_bind(self.tkId, BINDRIGHTBUTT, self.displayMenu)
        self.getCanvas().tag_bind(self.tkId, BINDENTER,
                                  lambda e: self.getMain().changeInfoLabelText(OBJECTINFO.format(self.type)))
        self.getCanvas().tag_bind(self.tkId, BINDLEAVE,
                                  lambda e: self.getMain().changeInfoLabelText(OBJECTINFOEMPTY))

    def lift(self):
        self.getCanvas().tag_raise(self.tkId)

    def onDoubleClick(self, _):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0
        self.draw()

    def changeIndex(self, index):
        self.index = index

    def getMain(self):
        return self.parent.parent.parent

    def displayMenu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root, 0)

    def createMenu(self):
        self.menu = tk.Menu(self.getCanvas(), tearoff=0)
        self.menu.add_command(label=CHANGEIMAGES, command=self.changeImages)
        self.menu.add_command(label=CHANGEORDERIMAGES, command=self.changeOrderImages)

        self.menu.add_separator()
        text = DESELECT if self.parent.selected else SELECT
        self.menu.add_command(label=text, command=self.toggle)
        self.menu.add_command(label=COPY, command=self.copy)
        self.menu.add_command(label=ROTATE, command=self.rotate)
        self.menu.add_command(label=REMOVEOBJECT, command=self.remove)
        self.menu.add_separator()
        self.menu.add_command(label=CREATEGRID, command=self.createGrid)

    def createGrid(self):
        self.parent.parent.parent.showCreateGridScreen(self)

    def changeImages(self, resetRot=True):
        imagePaths = askopenfilenames(title=CHOOSEIMAGES, initialdir=os.getcwd(), filetypes=FILETYPES)
        if len(imagePaths) > 0 and len(imagePaths) <= CLICKABLEMAX:
            self.images = []
            self.imgObjs = []
            self.imagesOrig = []
            self.index = 0
            for iimage in imagePaths:
                i = Image.open(iimage).resize((self.width, self.height))
                self.images.append(i)
                self.imagesOrig.append(i)
                self.imgObjs.append(ImageTk.PhotoImage(i))

            self.draw()

        if len(imagePaths) > CLICKABLEMAX:
            messagebox.showerror(title=ERROR, message=LIMITEXCEEDED)

    def changeImages2(self, imagePaths, resetRot=True):
        if imagePaths:
            self.images = []
            self.imgObjs = []
            for iimage in imagePaths:
                i = Image.open(iimage).resize((self.width, self.height))
                self.images.append(i)
                self.imgObjs.append(ImageTk.PhotoImage(i))

            self.draw()

    def changeImages3(self, images):
        if images:
            self.images = images
            self.imgObjs = []
            for iimage in images:
                self.imgObjs.append(ImageTk.PhotoImage(iimage))
            self.draw()

    def changeOrderImages(self):
        self.parent.parent.parent.showchangeOrderImagesScreen(self)

    def updateImages(self):
        self.getCanvas().delete(self.tkId)

        for i in range(len(self.images)):
            self.images[i] = self.imagesOrig[i].resize((self.width, self.height))
            self.imgObjs[i] = ImageTk.PhotoImage(self.images[i])

        self.tkId = self.createImage()
        self.setBinds()

    def onDrag(self, event):
        self.dragged = True
        self.move(event.x, event.y)

    def changeWidth(self, value, drawBorder=True):
        self.width = value
        self.updateImages()
        if drawBorder:
            self.drawSelectBorder()

    def changeHeight(self, value, drawBorder=True):
        self.height = value
        self.updateImages()
        if drawBorder:
            self.drawSelectBorder()

    def drawSelectBorder(self):
        self.getCanvas().delete(self.tkSelectId)
        self.tkSelectId = self.getCanvas().create_rectangle(self.x - (self.width / 2),
                                                            self.y - (self.height / 2), self.x + (self.width / 2),
                                                            self.y + (self.height / 2), width=2)

    def hide(self):
        self.getCanvas().itemconfig(self.tkId, state=HIDDEN)

    def show(self):
        self.getCanvas().itemconfig(self.tkId, state=NORMAL)

    def toggle(self):
        self.getCanvas().tkraise(self.tkId)
        if not self.parent.selected:
            self.select()
            self.getMain().addItemScales(self.width, self.height, self)
        else:
            self.getMain().removeItemScales()
            self.unselect()
        self.createMenu()

    def select(self):
        self.parent.parent.unselectAll()
        self.parent.selected = True
        self.parent.parent.selected = self.parent
        self.drawSelectBorder()

    def unselect(self):
        self.parent.selected = False
        self.parent.parent.selected = None
        self.getCanvas().delete(self.tkSelectId)

    def getTkId(self):
        return self.tkId

    def getCanvas(self):
        return self.parent.getInnerCanvas()

    def setX(self, value):
        self.x = value

    def setY(self, value):
        self.y = value

    def remove(self):
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)
        self.parent.remove()

    def move(self, x, y):
        self.setX(x)
        self.setY(y)
        # self.getCanvas().coords(self.tkId, x, y)
        # self.getCanvas().tkraise(self.tkId)
        # if self.parent.selected:
        #     self.drawSelectBorder()

    def render(self):
        if self.renderedX != self.x or self.renderedY != self.y:
            self.getCanvas().coords(self.tkId, self.x, self.y)
            self.getCanvas().tkraise(self.tkId)
            self.renderedX = self.x
            self.renderedY = self.y
            if self.parent.selected:
                self.drawSelectBorder()

        self.getCanvas().update()
        self.getCanvas().after(5, self.render)

    def toJson(self):
        obj = dict()
        obj[JSONX] = self.x
        obj[JSONY] = self.y
        obj[JSONWIDTH] = self.width
        obj[JSONHEIGHT] = self.height
        obj[JSONTYPE] = types[self.type]
        imagesText = []
        for image in self.images:
            imagesText.append(imageToText(image))

        obj[JSONIMAGES] = imagesText
        return obj
