from Constants import *


class GridObject:
    def __init__(self, parent, x, y, w, h, canvas, color):
        self.parent = parent
        self.canvas = canvas
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.tkId = 0
        self.type = JSONGRID
        self.draw()

    def setBinds(self):
        self.canvas.tag_bind(self.tkId, BINDRIGHTBUTT, self.removeFromCanvas)

    def removeFromCanvas(self, _):
        self.parent.removeGrid(self)
        self.parent.afterClicked = True

    def insideObject(self, x, y):
        halfHeight = self.height / 2
        halfWidth = self.width / 2
        if (self.x - halfWidth - 20) <= x <= (self.x + halfWidth + 20) and \
                (self.y - halfHeight - 20) <= y <= (self.y + halfHeight + 20):
            return True
        return False

    def draw(self):
        self.remove()
        halfH = self.height / 2
        halfW = self.width / 2
        self.tkId = self.canvas.create_rectangle(self.x - halfW, self.y - halfH, self.x + halfW,
                                                 self.y + halfH, outline=self.color, width=2)
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
        obj[JSONCOLOR] = self.color[1]
        return obj
