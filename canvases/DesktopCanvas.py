import os
from Constants import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename, askopenfilenames
from canvas_objects.CanvasObject import CanvasObject
from serializeImg import imageToText
import json
from tkcolorpicker import askcolor
from tkinter import messagebox
from CommonFunctions import strip_accents_list
from canvas_objects.HomeObject import HomeObject
from canvas_objects.GridObject import GridObject


class DesktopCanvas:
    def __init__(self, parent, parentCanvas, w, h):
        self.parentCanvas = parentCanvas
        self.parent = parent
        self.objects = []
        self.homes = []
        self.grids = []
        self.bgTkId = 0
        self.bgColor = DESKTOPBGCOLOR
        self.windowHeight = WHEIGHT
        self.windowWidth = WWIDTH
        self.canvasWidth = w
        self.canvasHeight = h
        self.bgImage = None
        self.afterClicked = False
        self.bgTkId = 0
        self.borderTkId = 0
        self.imgObj = None
        self.selected = None
        self.homesVisible = True
        self.x, self.y = 0, 0
        self.menuX, self.menuY = 0, 0
        self.mouseX, self.mouseY = 0, 0
        self.innerCanvas = tk.Canvas(self.parentCanvas, width=CWIDTH, height=CHEIGHT, bg=DESKTOPBGCOLOR, takefocus=0,
                                     highlightthickness=0)
        self.innerWindow = self.parentCanvas.create_window(0, 0, anchor=NW, window=self.innerCanvas)
        self.drawBorder()
        self.createMenu()
        self.setBinds()
        self.addObject(["images/1.png", "images/pic.png", "images/transparentBg.png",
                        "images/buttons/button.png", "images/buttons/copy.png",
                        "images/1.png", "images/2.png", "images/buttons/enlarge.png",
                        "images/buttons/delete.png"], CLICKABLE, 1295, 630)
        self.addObject(EMPTYSTRING, TEXTTYPE, 887, 320)
        self.addObject("images/pic.png", CLONABLE, 300, 300)

    def setBinds(self):
        self.innerCanvas.bind(BINDRIGHTBUTT, self.displayMenu)
        self.innerCanvas.bind(BINDMOTION, self.mouseMotion)
        self.innerCanvas.bind_all(BINDDELETE, self.deleteAllSelected)

    def resizeCanvasHeight(self, value):
        self.canvasHeight = value
        self.innerCanvas.configure(height=self.canvasHeight)
        self.parent.canvasLabel.configure(text=CANVASSIZE.format(self.canvasWidth, self.canvasHeight))
        self.updateBgImage()
        self.drawBorder()

    def addHome(self, x, y, w, h, vis=NORMAL):
        self.homes.append(HomeObject(self, x, y, w, h, self.innerCanvas, vis))

    def addGrid(self, x, y, w, h, color):
        self.grids.append(GridObject(self, x, y, w, h, self.innerCanvas, color))

    def removeHome(self, home):
        for i in range(len(self.homes)):
            if self.homes[i].tkId == home.tkId:
                self.homes[i].remove()
                self.homes.pop(i)
                break

    def removeGrid(self, grid):
        for i in range(len(self.grids)):
            if self.grids[i].tkId == grid.tkId:
                self.grids[i].remove()
                self.grids.pop(i)
                break

    def dropToHome(self, x, y):
        for home in self.homes:
            if home.insideObject(x, y):
                return home
        return None

    def resizeCanvasWidth(self, value):
        self.canvasWidth = value
        self.innerCanvas.configure(width=self.canvasWidth)
        self.parent.canvasLabel.configure(text=CANVASSIZE.format(self.canvasWidth, self.canvasHeight))

        self.updateBgImage()
        self.drawBorder()

    def createMenu(self):
        self.menu = tk.Menu(self.innerCanvas, tearoff=0)
        self.menu.add_command(label=ADDSTATIC, command=lambda: self.addPictureObject(STATIC))
        self.menu.add_command(label=ADDDRAGGABLE, command=lambda: self.addPictureObject(DRAGGABLE))
        self.menu.add_command(label=ADDCLONABLE, command=lambda: self.addPictureObject(CLONABLE))
        self.menu.add_command(label=ADDCLICKABLE, command=lambda: self.addPictureObject(CLICKABLE))
        self.menu.add_command(label=ADDTEXT, command=self.addTextObject)
        self.menu.add_separator()
        if self.bgImage is not None:
            self.menu.add_command(label=REMOVEBGIMG, command=self.removeBgImage)
            self.menu.add_command(label=CHANGEBGIMG, command=self.setBgImage)
        else:
            self.menu.add_command(label=SETBGIMG, command=self.setBgImage)

        if self.homesVisible:
            self.menu.add_command(label=HIDEHOMES, command=self.hideHomes)
        else:
            self.menu.add_command(label=SHOWHOMES, command=self.showHomes)
        self.menu.add_command(label=CHANGEBGCOLOR, command=self.setBgColor)

    def hideHomes(self):
        self.homesVisible = False
        for home in self.homes:
            home.hide()
        # self.createMenu()

    def showHomes(self):
        self.homesVisible = True
        for home in self.homes:
            home.show()
        # self.createMenu()

    def setBgColor(self):
        color = askcolor(self.bgColor, self.getCanvas(), title=CHOOSECOLOR)
        if color != (None, None):
            color = color[1]
            self.bgColor = color
            self.innerCanvas.configure(bg=color)

    def setBgColorNoAsk(self, color):
        self.innerCanvas.configure(bg=color)

    def deleteAllSelected(self, _):
        i = 0
        while i < len(self.objects):
            if self.objects[i].selected:
                self.objects[i].obj.remove()
                i -= 1
            i += 1
        self.parent.removeItemScales()

    def removeAllObjects(self):
        while len(self.objects) > 0:
            self.objects[0].obj.remove()

        while len(self.homes) > 0:
            self.homes[0].remove()
            self.homes.pop(0)

        while len(self.grids) > 0:
            self.grids[0].remove()
            self.grids.pop(0)

        self.innerCanvas.delete(ALL)

    def selectedCount(self):
        result = 0
        for obj in self.objects:
            if obj.selected:
                result += 1
        return result

    def getCanvas(self):
        return self.innerCanvas

    def mouseMotion(self, event):
        self.mouseX, self.mouseY = event.x, event.y
        self.parent.mouseLabel.configure(text=CURSORPOSITION.format(event.x, event.y))

    def removeObject(self, id):
        for i in range(len(self.objects)):
            if self.objects[i].id == id:
                self.objects.pop(i)
                break

    def setBgImage(self):
        path = askopenfilename(title=CHOOSEIMAGE, initialdir=os.getcwd(), filetypes=FILETYPES)
        if path:
            self.innerCanvas.delete(self.bgTkId)
            self.bgImage = Image.open(path)
            # self.bgImage = self.bgImage.resize((self.canvasWidth, self.canvasHeight))
            self.imgObj = ImageTk.PhotoImage(self.bgImage)
            self.bgTkId = self.innerCanvas.create_image(0, 0, image=self.imgObj, anchor='nw')
            self.innerCanvas.lower(self.bgTkId)
        # self.createMenu()

    def setBgImageNoAsk(self, img):
        self.innerCanvas.delete(self.bgTkId)
        self.bgImage = img
        self.imgObj = ImageTk.PhotoImage(self.bgImage)
        self.bgTkId = self.innerCanvas.create_image(0, 0, image=self.imgObj, anchor='nw')
        self.innerCanvas.lower(self.bgTkId)

    def removeBgImage(self):
        self.innerCanvas.delete(self.bgTkId)
        self.bgImage = None
        self.imgObj = None
        # self.createMenu()

    def updateBgImage(self):
        if self.bgImage is not None:
            self.innerCanvas.delete(self.bgTkId)
            # self.bgImage = self.bgImage.resize((self.canvasWidth, self.canvasHeight))
            self.imgObj = ImageTk.PhotoImage(self.bgImage)
            self.bgTkId = self.innerCanvas.create_image(0, 0, image=self.imgObj, anchor='nw')
            self.innerCanvas.lower(self.bgTkId)

    def hide(self):
        self.parentCanvas.itemconfig(self.innerWindow, state=HIDDEN)
        self.removeBorder()

    def show(self):
        self.parentCanvas.itemconfig(self.innerWindow, state=NORMAL)
        self.drawBorder()

    def isObjectAtPos(self, x, y):
        for obj in self.objects:
            if obj.insideObject(x, y):
                return True

        for obj in self.grids:
            if obj.insideObject(x, y):
                return True

        for obj in self.homes:
            if obj.insideObject(x, y):
                return True
        return False

    def displayMenu(self, event):
        self.createMenu()
        self.menuX, self.menuY = self.mouseX, self.mouseY
        if not self.isObjectAtPos(self.mouseX, self.mouseY) and not self.afterClicked:
            self.menu.tk_popup(event.x_root, event.y_root, 0)

        self.afterClicked = False

    def hideMenu(self):
        self.menu.unpost()

    def unselectAll(self):
        self.parent.removeItemScales()
        for obj in self.objects:
            obj.unselect()

    def addObject(self, value, typ, x, y):
        if typ == CLICKABLE and len(value) > CLICKABLEMAX:
            messagebox.showerror(title=ERROR, message=LIMITEXCEEDED)
            return
        else:
            if type(value) == str and typ != TEXTTYPE:
                value = Image.open(value)
            elif typ != TEXTTYPE:
                value = list(value)
                for i in range(len(value)):
                    value[i] = Image.open(value[i])

            obj = CanvasObject(self, value, typ, x, y)
            self.objects.append(obj)
            return obj

    def addObjectWithImages(self, value, typ, x, y):
        if typ == CLICKABLE and len(value) > CLICKABLEMAX:
            messagebox.showerror(title=ERROR, message=LIMITEXCEEDED)
            return
        else:
            obj = CanvasObject(self, value, typ, x, y)
            self.objects.append(obj)
            return obj

    def addPictureObject(self, typ):
        if typ == DRAGGABLE or typ == STATIC or typ == CLONABLE:
            path = askopenfilename(title=CHOOSEIMAGE, initialdir=os.getcwd(), filetypes=FILETYPES)
        else:
            path = askopenfilenames(title=CHOOSEIMAGES, initialdir=os.getcwd(), filetypes=FILETYPES)

        if (path and typ != CLICKABLE) or (typ == CLICKABLE and len(path) > 0 and len(path) <= CLICKABLEMAX):
            self.addObject(path, typ, self.menuX, self.menuY)

        if typ == CLICKABLE and len(path) > CLICKABLEMAX:
            messagebox.showerror(title=ERROR, message=LIMITEXCEEDED)

    def addTextObject(self):
        self.addObject(EMPTYSTRING, TEXTTYPE, self.menuX, self.menuY)

    def getMousePosX(self):
        return self.getCanvas().winfo_pointerx() - self.getCanvas().winfo_rootx()

    def getMousePosY(self):
        return self.getCanvas().winfo_pointery() - self.getCanvas().winfo_rooty()

    def getMousePosXY(self):
        return self.getMousePosX(), self.getMousePosY()

    def drawBorder(self):
        self.removeBorder()
        self.borderTkId = self.parent.getCanvas().create_rectangle(0, 0, self.canvasWidth, self.canvasHeight,
                                                                   outline=PRIMARYCOLOR, width=5)

    def removeBorder(self):
        self.parent.getCanvas().delete(self.borderTkId)

    def lower(self):
        self.parent.getCanvas().tag_lower(self.innerWindow)

    def createRectangle(self, x, y, w, h, color, dx=2):
        return self.innerCanvas.create_rectangle(x - (w / 2) - dx, y - (h / 2) - dx, x + (w / 2) + dx, y + (h / 2) + dx,
                                                 outline=color, width=2)

    def toJson(self):
        dictJson = dict()
        dictJson[JSONOBJECTS] = []
        dictJson[GRIDOBJECTS] = []
        dictJson[HOMEOBJECTS] = []
        for obj in self.objects:
            objDict = obj.toJson()
            dictJson[JSONOBJECTS].append(objDict)

        for obj in self.homes:
            objDict = obj.toJson()
            dictJson[HOMEOBJECTS].append(objDict)

        for grid in self.grids:
            gridDict = grid.toJson()
            dictJson[GRIDOBJECTS].append(gridDict)

        dictJson[JSONWIDTH] = self.canvasWidth
        dictJson[JSONHEIGHT] = self.canvasHeight
        textImg = None
        if self.bgImage is not None:
            textImg = imageToText(self.bgImage)
        dictJson[JSONBGIMAGE] = textImg
        dictJson[JSONBGCOLOR] = self.bgColor
        dictJson[JSONAVILBUTT] = strip_accents_list(self.parent.availButtons)
        dictJson[JSONHOMESVIS] = self.homesVisible

        dictStr = json.dumps(dictJson, indent=4)
        result = json.loads(dictStr)
        return result, dictStr
