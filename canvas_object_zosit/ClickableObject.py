from PIL import ImageTk, Image
import copy
from serializeImg import imageToText
from Constants import *


class ClickableObject:
    def __init__(self, parent, images, x, y, typ):
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
        self.draw()
        self.setBinds()

    def draw(self):
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)
        self.tkId = self.createImage()
        if self.parent.selected:
            self.drawSelectBorder()
        self.setBinds()

    def createImage(self):
        return self.getCanvas().create_image(self.x, self.y, image=self.imgObjs[self.index], anchor=CENTER)

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
        self.getCanvas().tag_bind(self.tkId, BINDLEFTBUTT, self.onClick)

    def lift(self):
        self.getCanvas().tag_raise(self.tkId)

    def onClick(self, _):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0
        self.draw()

    def changeIndex(self, index):
        self.index = index

    def updateImages(self):
        self.getCanvas().delete(self.tkId)

        for i in range(len(self.images)):
            self.images[i] = self.imagesOrig[i].resize((self.width, self.height))
            self.imgObjs[i] = ImageTk.PhotoImage(self.images[i])

        self.tkId = self.createImage()
        self.setBinds()

    def drawSelectBorder(self):
        self.getCanvas().delete(self.tkSelectId)
        self.tkSelectId = self.getCanvas().create_rectangle(self.x - (self.width / 2),
                                                            self.y - (self.height / 2), self.x + (self.width / 2),
                                                            self.y + (self.height / 2), width=2)

    def show(self):
        self.getCanvas().itemconfig(self.tkId, state=NORMAL)

    def toggle(self):
        self.getCanvas().tkraise(self.tkId)
        if not self.parent.selected:
            self.select()
        else:
            self.unselect()

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
        return self.parent.getCanvas()

    def setX(self, value):
        self.x = value

    def setY(self, value):
        self.y = value

    def remove(self):
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)
        self.parent.remove()

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
