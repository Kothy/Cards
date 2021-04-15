from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import tkinter as tk
import os
from Constants import *
import copy
from serializeImg import imageToText


class StaticDraggableObject:
    def __init__(self, parent, img, x, y, typ):
        self.parent = parent
        self.img = img
        self.imgOrig = img
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.type = typ
        self.x = x
        self.y = y
        self.renderedX = self.x
        self.renderedY = self.y
        self.width, self.height = self.img.size
        self.tkSelectId = 0
        self.tkId = 0
        self.draw()
        self.setBinds()
        if self.type == DRAGGABLE:
            self.render()

    def draw(self):
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)
        self.tkId = self.getCanvas().create_image(self.x, self.y, image=self.imgObj, anchor='c')
        self.setBinds()

    def copy(self, x=None, y=None):
        newX = self.x + 30 if x is None else x
        newY = self.y + 30 if y is None else y
        newObject = self.parent.parent.addObjectWithImage(self.img, self.type, newX, newY)
        newObject = newObject.getObject()
        newObject.typ = copy.copy(self.type)
        newObject.changeWidth(copy.copy(self.width))
        newObject.changeHeight(copy.copy(self.height))
        newObject.draw()

    def rotate(self, deg=90):
        self.img = self.img.rotate(deg, expand=True)
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.width, self.height = self.height, self.width
        self.draw()

    def flipHorizontally(self):
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.draw()

    def flipVertically(self):
        self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.draw()

    def lift(self):
        self.getCanvas().tag_raise(self.tkId)

    def setBinds(self):
        if self.type == DRAGGABLE:
            self.getCanvas().tag_bind(self.tkId, BINDLEFTBUTT, self.onClick)
            self.getCanvas().tag_bind(self.tkId, BINDRIGHTMOTION, self.onDrag)
            # self.getCanvas().tag_bind(self.tkId, BINDLEFTRELEASE, None)
            # self.getCanvas().tag_bind(self.tkId, BINDRIGHTBUTT, self.displayMenu)
            self.getCanvas().tag_bind(self.tkId, BINDLEFTRELEASE, self.onDrop)
            # self.getCanvas().tag_bind(self.tkId, BINDENTER,
            #                           lambda e: self.getMain().changeInfoLabelText(OBJECTINFO.format(self.type)))
            # self.getCanvas().tag_bind(self.tkId, BINDLEAVE,
            #                           lambda e: self.getMain().changeInfoLabelText(OBJECTINFOEMPTY))

    def getMain(self):
        return self.parent.parent.parent

    def updateImage(self):
        self.getCanvas().delete(self.tkId)
        self.img = self.imgOrig.resize((self.width, self.height))
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.tkId = self.getCanvas().create_image(self.x, self.y, image=self.imgObj, anchor='c')
        self.setBinds()

    def onClick(self, _):
        fun = self.parent.parent.selectedFunction
        if fun is not None:
            if fun == COPY:
                self.copy(self.x + 20, self.y + 20)
            elif fun == PASTE:
                print(self.parent.parent.selectedFunction)
            elif fun == REMOVEOBJECT:
                self.remove()
            elif fun == UPSIZE:
                self.parent.parent.addScales()
            elif fun == DOWNSIZE:
                self.parent.parent.addScales(self)
            elif fun == FLIPVERTICALLY:
                self.flipVertically()
            elif fun == FLIPHORIZONTALLY:
                self.flipHorizontally()

    def onDrag(self, event):
        if self.parent.parent.selectedFunction is None:
            self.move(event.x, event.y)

    def onDrop(self, _):
        if self.parent.parent.selectedFunction is None:
            home = self.parent.parent.dropToHome(self.x, self.y)
            if home is not None:
                self.setX(home.x)
                self.setY(home.y)

    def changeWidth(self, value):
        self.width = value
        self.updateImage()

    def changeHeight(self, value):
        self.height = value
        if self.parent.parent.scale1 is not None:
            self.parent.parent.scale1.place(x=self.x, y=self.y + self.height / 2, anchor=CENTER)
            self.parent.parent.scale2.place(x=self.x, y=self.y + self.height / 2 + 35, anchor=CENTER)
        self.updateImage()

    def hide(self):
        self.getCanvas().itemconfig(self.tkId, state=HIDDEN)

    def show(self):
        self.getCanvas().itemconfig(self.tkId, state=NORMAL)

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

    def renderMove(self):
        self.move(self.x, self.y)
        self.getCanvas().after(10, self.renderMove)

    def move(self, x, y):
        if self.type == DRAGGABLE:
            self.setX(x)
            self.setY(y)

    def render(self):
        if self.renderedX != self.x or self.renderedY != self.y:
            self.getCanvas().coords(self.tkId, self.x, self.y)
            self.getCanvas().tkraise(self.tkId)
            self.renderedX = self.x
            self.renderedY = self.y

        self.getCanvas().update()
        self.getCanvas().after(5, self.render)

    def toJson(self):
        obj = dict()
        obj[JSONX] = self.x
        obj[JSONY] = self.y
        obj[JSONWIDTH] = self.width
        obj[JSONHEIGHT] = self.height
        obj[JSONTYPE] = types[self.type]
        obj[JSONIMAGE] = imageToText(self.img)
        return obj
