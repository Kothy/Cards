from PIL import ImageTk, Image
from Constants import *
from CommonFunctions import strip_accents
from canvases.CheckboxCanvas import CheckboxCanvas


class AvailableButtonsScreen:
    def __init__(self, parent, command):
        self.parent = parent
        self.command = command
        self.transImg = Image.open(IMAGETRANSPARENT)
        self.transImg = self.transImg.resize((self.parent.windowWidth, self.parent.windowHeight))
        self.transImgObj = ImageTk.PhotoImage(self.transImg)
        self.transBgTkId = 0
        self.checkboxes = CheckboxCanvas(self, self.parent.getCanvas(), self.command)

    def show(self):
        self.transBgTkId = self.parent.getCanvas().create_image(0, 0, image=self.transImgObj, anchor='nw')
        self.parent.getCanvas().tkraise(self.transBgTkId)
        self.checkboxes.show()

    def hide(self):
        self.checkboxes.hide()
        self.parent.getCanvas().delete(self.transBgTkId)

    def drawButtons(self, array, canvas):
        paths = list()
        x = 0.6
        y = 0.5
        h = 30
        width = self.parent.windowWidth
        dx = 0.03
        for (check, var, name) in self.checkboxes.checkbuttons:
            if var.get():
                # if strip_accents(name) == strip_accents(UPSIZE):
                #     array.append(name)
                #     canvas.addImage(ICOUPSIZE, x, y, width / 48, h, name, None, True, "c", rel=True)
                #     paths.append(ICOUPSIZE)
                # if strip_accents(name) == strip_accents(DOWNSIZE):
                #     array.append(name)
                #     canvas.addImage(ICODOWNSIZE, x, y, width / 48, h, name, None, True, "c", rel=True)
                #     paths.append(ICODOWNSIZE)
                if strip_accents(name) == strip_accents(RESIZE):
                    array.append(name)
                    canvas.addImage(ICONRESIZE, x, y, width / 48, h, name, None, True, "c", rel=True)
                    paths.append(ICONRESIZE)
                if strip_accents(name) == strip_accents(FLIPHORIZONTALLY):
                    array.append(name)
                    canvas.addImage(ICOFLIPH, x, y, width / 48, h, name, None, True, "c", rel=True)
                    paths.append(ICOFLIPH)
                if strip_accents(name) == strip_accents(FLIPVERTICALLY):
                    array.append(name)
                    paths.append(ICOFLIPV)
                    canvas.addImage(ICOFLIPV, x, y, width / 48, h, name, None, True, "c", rel=True)
                if strip_accents(name) == strip_accents(COPYPASTE):
                    array.append(name)
                    paths.append(ICOCOPY)
                    paths.append(ICOPASTE)
                    canvas.addImage(ICOCOPY, x, y, width / 48, h, COPY, None, True, "c", rel=True)
                    canvas.addImage(ICOPASTE, x + dx, y, width / 48, h, PASTE, None, True, "c", rel=True)
                    x += dx
                if strip_accents(name) == strip_accents(REMOVEOBJECT):
                    array.append(name)
                    paths.append(ICOREMOVE)
                    canvas.addImage(ICOREMOVE, x, y, width / 48, h, name, None, True, "c", rel=True)
                x += dx

        return paths

    def drawButtonsWithArray(self, array, canvas):
        x = 0.6
        y = 0.5
        h = 30
        width = self.parent.windowWidth
        dx = 0.03
        for name in array:
            # if strip_accents(name) == strip_accents(UPSIZE):
            #     canvas.addImage(ICOUPSIZE, x, y, width / 48, h, name, None, True, "c", rel=True)
            # if strip_accents(name) == strip_accents(DOWNSIZE):
            #     canvas.addImage(ICODOWNSIZE, x, y, width / 48, h, name, None, True, "c", rel=True)
            if strip_accents(name) == strip_accents(RESIZE):
                canvas.addImage(ICONRESIZE, x, y, width / 48, h, name, None, True, "c", rel=True)
            if strip_accents(name) == strip_accents(FLIPHORIZONTALLY):
                canvas.addImage(ICOFLIPH, x, y, width / 48, h, name, None, True, "c", rel=True)
            if strip_accents(name) == strip_accents(FLIPVERTICALLY):
                canvas.addImage(ICOFLIPV, x, y, width / 48, h, name, None, True, "c", rel=True)
            if strip_accents(name) == strip_accents(COPYPASTE):
                canvas.addImage(ICOCOPY, x, y, width / 48, h, COPY, None, True, "c", rel=True)
                canvas.addImage(ICOPASTE, x + dx, y, width / 48, h, PASTE, None, True, "c", rel=True)
                x += dx
            if strip_accents(name) == strip_accents(REMOVEOBJECT):
                canvas.addImage(ICOREMOVE, x, y, width / 48, h, name, None, True, "c", rel=True)
            x += dx
