from PIL import ImageTk
from Constants import *
import copy
from serializeImg import imageToText


class ClonableObject:
    def __init__(self, parent, img, x, y, typ):
        self.parent = parent
        self.img = img
        self.imgOrig = img
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.type = typ
        self.clonedObject = None
        self.x = x
        self.y = y
        self.gridBorder = []
        self.renderedX = self.x
        self.renderedY = self.y
        self.width, self.height = self.img.size
        self.tkSelectId = 0
        self.tkId = 0
        self.mode = CLONABLE
        self.draw()
        self.setBinds()

    def draw(self):
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)
        self.tkId = self.getCanvas().create_image(self.x, self.y, image=self.imgObj, anchor=CENTER)
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

    def clone(self):
        newObject = self.parent.parent.addObjectWithImage(self.img, DRAGGABLE, self.x + 10, self.y + 10)
        newObject = newObject.getObject()
        newObject.cloneParent = self
        self.clonedObject = newObject
        newObject.typ = copy.copy(DRAGGABLE)
        newObject.changeWidth(copy.copy(self.width))
        newObject.changeHeight(copy.copy(self.height))
        newObject.draw()

    def setBinds(self):
        self.getCanvas().tag_bind(self.tkId, BINDLEFTBUTT, self.onClick)
        self.getCanvas().tag_bind(self.tkId, BINDRIGHTMOTION, self.onDrag)
        self.getCanvas().tag_bind(self.tkId, BINDLEFTRELEASE, self.onDragRelease)

    def onDrag(self, event):
        if self.clonedObject is not None:
            self.clonedObject.lift()
            self.clonedObject.onDrag(event)

    def onDragRelease(self, _):
        self.clonedObject = None

    def displayInfo(self, _):
        self.getMain().changeInfoLabelText(OBJECTINFO.format("{}, Mód: {}".format(self.type, self.mode)))

    def onClick(self, _):
        self.clone()

    def getMain(self):
        return self.parent.parent.parent

    def rotate(self, deg=90):
        self.img = self.img.rotate(deg, expand=True)
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.width, self.height = self.height, self.width
        self.draw()

    def updateImage(self):
        self.getCanvas().delete(self.tkId)
        self.img = self.imgOrig.resize((self.width, self.height))
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.tkId = self.getCanvas().create_image(self.x, self.y, image=self.imgObj, anchor='c')
        self.setBinds()

    def lift(self):
        self.getCanvas().lift(self.tkId)
        self.getCanvas().tag_raise(self.tkId)

    def lower(self):
        self.getCanvas().lower(self.tkId, self.parent.parent.bgTkId)

    def hide(self):
        self.getCanvas().itemconfig(self.tkId, state=HIDDEN)

    def show(self):
        self.getCanvas().itemconfig(self.tkId, state=NORMAL)

    def getTkId(self):
        return self.tkId

    def getCanvas(self):
        return self.parent.parent.canvas

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
        obj[JSONIMAGE] = imageToText(self.img)
        return obj
