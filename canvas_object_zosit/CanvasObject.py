from canvas_object_zosit.StaticDraggableObject import StaticDraggableObject
from canvas_object_zosit.TextObject import TextObject
from canvas_object_zosit.ClickableObject import ClickableObject
from canvas_object_zosit.ClonableObject import ClonableObject
from Constants import *


class CanvasObject:
    def __init__(self, parent, value, typ, x, y):
        global OBJID
        self.parent = parent
        self.selected = False
        self.id = OBJID
        OBJID += 1
        if typ == STATIC or typ == DRAGGABLE:
            self.obj = StaticDraggableObject(self, value, x, y, typ)
        elif typ == CLONABLE:
            self.obj = ClonableObject(self, value, x, y, typ)
        elif typ == CLICKABLE:
            self.obj = ClickableObject(self, value, x, y, typ)
        elif typ == TEXTTYPE:
            self.obj = TextObject(self, x, y)
        else:
            self.obj = None

    def hide(self):
        self.obj.hide()

    def getHeight(self):
        return self.obj.height

    def getWidth(self):
        return self.obj.width

    def copy(self):
        self.obj.copy()

    def select(self):
        self.obj.select()

    def unselect(self):
        self.obj.unselect()

    def downSize(self):
        self.obj.downSize()

    def changeHeight(self, value):
        self.obj.changeHeight(value)

    def changeWidth(self, value):
        self.obj.changeWidth(value)

    def getCanvas(self):
        return self.parent.getCanvas()

    def getInnerCanvas(self):
        return self.parent.getCanvas()

    # def getMousePosX(self):
    #     return self.parent.getMousePosX()
    #
    # def getMousePosY(self):
    #     return self.parent.getMousePosY()

    def getObject(self):
        return self.obj

    # def getMousePosXY(self):
    #     return self.getMousePosX(), self.getMousePosY()

    def remove(self):
        global IMGREMOVE
        self.parent.removeObject(self.id)
        IMGREMOVE = True

    def insideObject(self, x, y):
        halfHeight = self.obj.height / 2
        halfWidth = self.obj.width / 2

        if (self.obj.x - halfWidth) <= x <= (self.obj.x + halfWidth) and \
                (self.obj.y - halfHeight) <= y <= (self.obj.y + halfHeight):
            return True
        return False

    def toJson(self):
        return self.obj.toJson()
