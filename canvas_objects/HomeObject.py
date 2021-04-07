from Constants import *


class HomeObject:
    def __init__(self, parent, x, y, w, h, canvas, visibility=NORMAL):
        self.parent = parent
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.tkId = 0
        self.type = HOME
        if visibility == NORMAL:
            self.draw()

    def setBinds(self):
        self.canvas.tag_bind(self.tkId, BINDRIGHTBUTT, self.removeFromCanvas)

    def removeFromCanvas(self, _):
        self.parent.removeHome(self)
        self.parent.afterClicked = True

    def insideObject(self, x, y):
        halfHeight = self.height / 2
        halfWidth = self.width / 2
        if (self.x - halfWidth) <= x <= (self.x + halfWidth) and \
                (self.y - halfHeight) <= y <= (self.y + halfHeight):
            return True
        return False

    def draw(self):
        self.remove()
        halfH = self.height / 2
        halfW = self.width / 2
        self.tkId = self.canvas.create_rectangle(self.x - halfW - 2, self.y - halfH - 2, self.x + halfW + 2, self.y + halfH + 2,
                                                 outline=BLACK, width=2)
        self.setBinds()

    def remove(self):
        self.canvas.delete(self.tkId)

    def hide(self):
        self.remove()

    def show(self):
        self.draw()

    def toJson(self):
        obj = dict()
        obj[JSONX] = self.x
        obj[JSONY] = self.y
        obj[JSONWIDTH] = self.width
        obj[JSONHEIGHT] = self.height
        obj[JSONTYPE] = self.type
        return obj
