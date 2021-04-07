from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import tkinter as tk
import os
from Constants import *
import copy
from serializeImg import imageToText


class StaticDraggableObject:
    def __init__(self, parent, img, x, y, typ):  # draggable and static
        self.parent = parent
        self.img = img
        self.imgOrig = img
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.type = typ
        self.x = x
        self.y = y
        self.gridBorder = []
        self.renderedX = self.x
        self.renderedY = self.y
        self.width, self.height = self.img.size
        self.tkSelectId = 0
        self.tkId = 0
        self.createMenu()
        self.draw()
        self.setBinds()
        self.render()

    def draw(self):
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)
        self.tkId = self.getCanvas().create_image(self.x, self.y, image=self.imgObj, anchor='c')
        if self.parent.selected:
            self.drawSelectBorder()
        self.setBinds()

    def copy(self, x=None, y=None):
        newX = self.x + 30 if x is None else x
        newY = self.y + 30 if y is None else y
        newObject = self.parent.parent.addObjectWithImages(self.img, self.type, newX, newY)
        newObject = newObject.getObject()
        newObject.typ = copy.copy(self.type)
        newObject.changeWidth(copy.copy(self.width), False)
        newObject.changeHeight(copy.copy(self.height), False)
        newObject.draw()

    def rotate(self, deg=90):
        self.img = self.img.rotate(deg, expand=True)
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.width, self.height = self.height, self.width
        if self.parent.selected:
            self.drawSelectBorder()
        self.draw()

    def flipHorizontally(self):
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)
        self.imgObj = ImageTk.PhotoImage(self.img)
        if self.parent.selected:
            self.drawSelectBorder()
        self.draw()

    def flipVertically(self):
        self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        self.imgObj = ImageTk.PhotoImage(self.img)
        if self.parent.selected:
            self.drawSelectBorder()
        self.draw()

    def lift(self):
        self.getCanvas().tag_raise(self.tkId)

    def setBinds(self):
        self.getCanvas().tag_bind(self.tkId, BINDRIGHTMOTION, self.onDrag)
        self.getCanvas().tag_bind(self.tkId, BINDLEFTRELEASE, None)
        self.getCanvas().tag_bind(self.tkId, BINDRIGHTBUTT, self.displayMenu)
        self.getCanvas().tag_bind(self.tkId, BINDLEFTRELEASE, self.onDrop)
        self.getCanvas().tag_bind(self.tkId, BINDENTER,
                                  lambda e: self.getMain().changeInfoLabelText(OBJECTINFO.format(self.type)))
        self.getCanvas().tag_bind(self.tkId, BINDLEAVE,
                                  lambda e: self.getMain().changeInfoLabelText(OBJECTINFOEMPTY))

    def getMain(self):
        return self.parent.parent.parent

    def displayMenu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root, 0)

    def createMenu(self):
        self.menu = tk.Menu(self.getCanvas(), tearoff=0)
        self.menu.add_command(label=CHANGEIMAGE, command=self.changeImage)
        self.menu.add_separator()
        text = DESELECT if self.parent.selected else SELECT
        self.menu.add_command(label=text, command=self.toggle)
        self.menu.add_command(label=COPY, command=self.copy)
        self.menu.add_command(label=ROTATE, command=self.rotate)
        self.menu.add_command(label=FLIPVERTICALLY, command=self.flipVertically)
        self.menu.add_command(label=FLIPHORIZONTALLY, command=self.flipHorizontally)
        self.menu.add_command(label=REMOVEOBJECT, command=self.remove)
        self.menu.add_separator()
        self.menu.add_command(label=CREATEGRID, command=self.createGrid)
        self.menu.add_command(label=CREATEHOME, command=self.addHome)

    def addHome(self):
        self.parent.parent.addHome(self.x, self.y, self.width, self.height)

    def createGrid(self):
        self.parent.parent.parent.showCreateGridScreen(self)

    def changeImage(self):
        imagePath = askopenfilename(title=CHOOSEIMAGE, initialdir=os.getcwd(), filetypes=FILETYPES)
        if imagePath:
            self.getCanvas().delete(self.tkId)
            self.img = Image.open(imagePath)
            self.imgOrig = Image.open(imagePath)
            self.imgObj = ImageTk.PhotoImage(self.img)
            self.tkId = self.getCanvas().create_image(self.x, self.y, image=self.imgObj, anchor='c')
            self.setBinds()

    def updateImage(self):
        self.getCanvas().delete(self.tkId)
        self.img = self.imgOrig.resize((self.width, self.height))
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.tkId = self.getCanvas().create_image(self.x, self.y, image=self.imgObj, anchor='c')
        self.setBinds()

    def onDrag(self, event):
        self.move(event.x, event.y)

    def onDrop(self, _):
        home = self.parent.parent.dropToHome(self.x, self.y)
        if home is not None:
            self.setX(home.x)
            self.setY(home.y)

    def changeWidth(self, value, drawBorder=True):
        self.width = value
        self.updateImage()
        if drawBorder:
            self.drawSelectBorder()

    def changeHeight(self, value, drawBorder=True):
        self.height = value
        self.updateImage()
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

    def renderMove(self):
        self.move(self.x, self.y)
        self.getCanvas().after(10, self.renderMove)

    def move(self, x, y):
        self.setX(x)
        self.setY(y)
        # self.getCanvas().coords(self.tkId, x, y)
        #
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
        obj[JSONIMAGE] = imageToText(self.img)
        return obj
