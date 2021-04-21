import json
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, askopenfilename

from PIL import ImageTk, Image

from CommonFunctions import strip_accents_list, strip_accents
from Constants import *
from canvas_object_zosit.CanvasObject import CanvasObject
from canvas_objects.GridObject import GridObject
from canvas_objects.HomeObject import HomeObject
from canvases.BarCanvas import BarCanvas
from serializeImg import imageToText
from serializeImg import textToImage

icons = dict()
icons[COPY] = "images/buttons/eZositIcons/copy.png"
icons[PASTE] = "images/buttons/eZositIcons/paste.png"
icons[REMOVEOBJECT] = "images/buttons/eZositIcons/remove.png"
icons[FLIPVERTICALLY] = "images/buttons/eZositIcons/vflip.png"
icons[FLIPHORIZONTALLY] = "images/buttons/eZositIcons/hflip.png"
icons[UPSIZE] = "images/buttons/eZositIcons/enlarge.png"
icons[DOWNSIZE] = "images/buttons/eZositIcons/shrink.png"
icons[RESIZE] = "images/buttons/eZositIcons/resize.png"

icons_grey = dict()
icons_grey[COPY] = "images/buttons/eZositIcons/copy_grey.png"
icons_grey[PASTE] = "images/buttons/eZositIcons/paste_grey.png"
icons_grey[REMOVEOBJECT] = "images/buttons/eZositIcons/remove_grey.png"
icons_grey[FLIPVERTICALLY] = "images/buttons/eZositIcons/vflip_grey.png"
icons_grey[FLIPHORIZONTALLY] = "images/buttons/eZositIcons/hflip_grey.png"
icons_grey[UPSIZE] = "images/buttons/eZositIcons/enlarge_grey.png"
icons_grey[DOWNSIZE] = "images/buttons/eZositIcons/shrink_grey.png"
icons_grey[RESIZE] = "images/buttons/eZositIcons/resize_grey.png"

barWidth = WWIDTH - DESKTOPWMAX


class eZositScreen:
    def __init__(self, parentCanvas):
        self.parentCanvas = parentCanvas
        self.bgColor = WHITE
        self.scale1 = None
        self.scale2 = None
        self.canvas = tk.Canvas(self.parentCanvas, width=CWIDTH, height=CHEIGHT, bg=self.bgColor, takefocus=0,
                                highlightthickness=0)
        self.borderTkId = 0
        self.innerWindow = self.parentCanvas.create_window(0, 0, anchor=NW, window=self.canvas)
        self.availButtons = []
        self.canvasWidth = CWIDTH
        self.canvasHeight = CHEIGHT
        self.createRightBar()
        self.setParentCanvasSize(self.canvasWidth + barWidth + 5, WHEIGHT)
        self.iconH, self.iconW = barWidth - 30, barWidth - 10
        self.selectedTkId = None
        self.selectedFunction = None
        self.objects = []
        self.homes = []
        self.grids = []
        self.bgImage = None
        self.bgColor = WHITE
        self.drawBorder()
        self.homesVisible = False
        self.hover = None
        self.selected = None
        self.bgTkId = 0
        self.bgImage = None
        self.imgObj = None

        self.addObject(["images/1.png", "images/pic.png", "images/transparentBg.png",
                        "images/buttons/button.png", "images/buttons/copy.png",
                        "images/1.png", "images/2.png", "images/buttons/enlarge.png",
                        "images/buttons/delete.png"], CLICKABLE, 200, 200)

        self.addObject("images/pic.png", CLONABLE, 400, 400)
        fontSet = {
            UNDERLINE: False,
            OVERSTRIKE: False,
            WEIGHT: NORMAL,
            SLANT: ROMAN,
            SIZE: 20,
            FAMILY: DEFAULTFONT,
            COLOR: BLACK,
            JSONBGCOLOR: "purple"
        }
        self.addTextObject(600, 400, 100, 100, fontSet)
        self.addObject("images/2.png", STATIC, 600, 800)

    def resizeCanvasHeight(self, height):
        self.canvasHeight = height
        self.canvas.config(height=height)
        self.removeBorder()
        self.drawBorder()

    def resizeCanvasWidth(self, width):
        self.canvasWidth = width
        self.canvas.configure(width=width)
        self.removeBorder()
        self.drawBorder()

    def setBgColor(self, color):
        self.bgColor = color
        self.canvas.configure(bg=self.bgColor)

    def removeObject(self, id):
        for i in range(len(self.objects)):
            if self.objects[i].id == id:
                self.objects.pop(i)
                break

    def resizeObjHeight(self, _):
        self.selected.changeHeight(self.scaleVar2.get())

    def resizeObjWidth(self, _):
        self.selected.changeWidth(self.scaleVar1.get())

    def addScales(self, obj):
        if self.scale1 is None:
            self.selected = obj
            self.scaleVar1 = tk.IntVar()
            self.scaleVar2 = tk.IntVar()
            s1 = ttk.Style()
            self.scaleVar1.set(obj.width)
            self.scaleVar2.set(obj.height)
            s1.configure('Horizontal.TScale', background=PRIMARYCOLOR, activebackground=SECONDARYCOLOR)
            self.scale1 = ttk.Scale(self.canvas, command=self.resizeObjWidth, variable=self.scaleVar1, from_=10, to=300,
                                    orient=tk.HORIZONTAL, length=200, cursor=HORIZARROW, style="Horizontal.TScale")

            self.scale2 = ttk.Scale(self.canvas, command=self.resizeObjHeight, variable=self.scaleVar2, from_=10, to=300,
                                    orient=tk.HORIZONTAL, length=200, cursor=VERTICARROW, style="Horizontal.TScale")
            self.scale1.place(x=obj.x, y=obj.y + obj.height/2 + 15, anchor=CENTER)
            self.scale2.place(x=obj.x, y=obj.y + obj.height/2 + 50, anchor=CENTER)

    def addObject(self, value, typ, x, y):
        if type(value) == str and typ != TEXTTYPE:
            value = Image.open(value)
        elif typ != TEXTTYPE:
            value = list(value)
            for i in range(len(value)):
                value[i] = Image.open(value[i])

        obj = CanvasObject(self, value, typ, x, y)
        self.objects.append(obj)
        return obj

    def removeAllObjects(self):
        while len(self.objects) > 0:
            self.objects[0].obj.remove()

        while len(self.homes) > 0:
            self.homes[0].remove()
            self.homes.pop(0)

        while len(self.grids) > 0:
            self.grids[0].remove()
            self.grids.pop(0)

        self.canvas.delete(ALL)

    def addTextObject(self, x, y, w, h, fontSet):
        obj = CanvasObject(self, None, TEXTTYPE, x, y)
        self.objects.append(obj)
        obj.obj.setFontSet(fontSet[UNDERLINE], fontSet[OVERSTRIKE], fontSet[WEIGHT], fontSet[SLANT], fontSet[SIZE],
                           fontSet[FAMILY], fontSet[COLOR])
        obj.obj.changeHeight(h)
        obj.obj.changeWidth(w)
        obj.obj.text = "test text"
        obj.obj.bgColor = fontSet[JSONBGCOLOR]
        obj.obj.createTextEntry()
        return obj

    def addObjectWithImage(self, value, typ, x, y):
        obj = CanvasObject(self, value, typ, x, y)
        self.objects.append(obj)
        return obj

    def addGrid(self, x, y, w, h, color):
        self.grids.append(GridObject(self, x, y, w, h, self.canvas, color))

    def addHome(self, x, y, w, h, vis=NORMAL):
        self.homes.append(HomeObject(self, x, y, w, h, self.canvas, vis))

    def dropToHome(self, x, y):
        for home in self.homes:
            if home.insideObject(x, y):
                return home
        return None

    def createRightBar(self):
        # self.rightBar = BarCanvas(self, self.parentCanvas, WWIDTH - barWidth - 5, 0, PRIMARYCOLOR, barWidth, WHEIGHT)
        self.rightBar = BarCanvas(self, self.parentCanvas, CWIDTH + 5, 0, PRIMARYCOLOR, barWidth, WHEIGHT)
        self.loadRightBar()

    def moveRightBar(self):
        self.rightBar.canvas.destroy()
        self.rightBar = BarCanvas(self, self.parentCanvas, self.canvasWidth + 5, 0, PRIMARYCOLOR, barWidth, WHEIGHT)
        self.loadRightBar()

    def loadRightBar(self):
        arr = self.availButtons
        self.rightBar.removeAllImages()
        h, w = barWidth - 30, barWidth - 10
        x = 190
        space = 25
        dy = 10
        self.ys = []
        self.rightBar.addImage("images/buttons/eZositIcons/save.png", barWidth / 2,
                               10 + h / 2, w, h, SAVE, self.saveAs, True, anchor=CENTER,
                               enterComm=lambda x: self.nothing(SAVE), leaveComm=lambda x: self.nothing(SAVE))
        self.rightBar.addImage("images/buttons/eZositIcons/new.png", barWidth / 2, (20 + h * 1) + space,
                               w, h, LOADULOHA, self.loadeZosit, True, anchor=CENTER,
                               enterComm=lambda x: self.nothing(LOADULOHA),
                               leaveComm=lambda x: self.nothing(LOADULOHA))

        self.rightBar.addStaticImage("images/buttons/separator.png", barWidth / 2, (h * 2) + space, barWidth - 10, 2)
        y = x + space
        path = icons[COPY] if strip_accents(COPYPASTE) in arr else icons_grey[COPY]
        self.ys.append([y, path])
        self.rightBar.addImage(path, barWidth / 2, x + space, w, h, COPY,
                               lambda x: self.selectIcon(COPY), True, anchor=CENTER,
                               enterComm=lambda x: self.hoverIcon(COPY), leaveComm=self.unhoverIcon)

        y = (x + (h + dy)) + space
        path = icons[REMOVEOBJECT] if strip_accents(REMOVEOBJECT) in arr else icons_grey[REMOVEOBJECT]
        self.ys.append([y, path])
        self.rightBar.addImage(path, barWidth / 2, y,
                               w, h, REMOVEOBJECT, lambda x: self.selectIcon(REMOVEOBJECT), True,
                               anchor=CENTER, enterComm=lambda x: self.hoverIcon(REMOVEOBJECT),
                               leaveComm=self.unhoverIcon)

        # y = (x + (h + dy) * 2) + space
        # path = icons[UPSIZE] if strip_accents(UPSIZE) in arr else icons_grey[UPSIZE]
        # self.ys.append([y, path])
        # self.rightBar.addImage(path, barWidth / 2, y, w, h, UPSIZE, lambda x: self.selectIcon(UPSIZE), True,
        #                        anchor=CENTER, enterComm=lambda x: self.hoverIcon(UPSIZE), leaveComm=self.unhoverIcon)
        #
        # y = (x + (h + dy) * 3) + space
        # path = icons[DOWNSIZE] if strip_accents(DOWNSIZE) in arr else icons_grey[DOWNSIZE]
        # self.ys.append([y, path])
        # self.rightBar.addImage(path, barWidth / 2, y,
        #                        w, h, DOWNSIZE, lambda x: self.selectIcon(DOWNSIZE), True,
        #                        anchor=CENTER, enterComm=lambda x: self.hoverIcon(DOWNSIZE),
        #                        leaveComm=self.unhoverIcon)

        y = (x + (h + dy) * 2) + space
        path = icons[RESIZE] if strip_accents(RESIZE) in arr else icons_grey[RESIZE]
        self.ys.append([y, path])
        self.rightBar.addImage(path, barWidth / 2, y, w, h, RESIZE, lambda x: self.selectIcon(RESIZE), True,
                               anchor=CENTER, enterComm=lambda x: self.hoverIcon(RESIZE), leaveComm=self.unhoverIcon)

        y = (x + (h + dy) * 3) + space
        path = icons[FLIPVERTICALLY] if strip_accents(FLIPVERTICALLY) in arr else icons_grey[FLIPVERTICALLY]
        self.ys.append([y, path])
        self.rightBar.addImage(path, barWidth / 2, y, w,
                               h, FLIPVERTICALLY, lambda x: self.selectIcon(FLIPVERTICALLY), True,
                               anchor=CENTER, enterComm=lambda x: self.hoverIcon(FLIPVERTICALLY),
                               leaveComm=self.unhoverIcon)

        y = (x + (h + dy) * 4) + space
        path = icons[FLIPHORIZONTALLY] if strip_accents(FLIPHORIZONTALLY) in arr else icons_grey[FLIPHORIZONTALLY]
        self.ys.append([y, path])
        self.rightBar.addImage(path, barWidth / 2, y, w,
                               h, FLIPHORIZONTALLY, lambda x: self.selectIcon(FLIPHORIZONTALLY), True,
                               anchor=CENTER, enterComm=lambda x: self.hoverIcon(FLIPHORIZONTALLY),
                               leaveComm=self.unhoverIcon)

    def nothing(self, text):
        print(text)

    def getY(self, text):
        if text == COPY:
            return self.ys[0][0]
        elif text == REMOVEOBJECT:
            return self.ys[1][0]
        # elif text == UPSIZE:
        #     return self.ys[2][0]
        # elif text == DOWNSIZE:
        #     return self.ys[3][0]
        elif text == RESIZE:
            return self.ys[2][0]
        elif text == FLIPVERTICALLY:
            return self.ys[3][0]
        elif text == FLIPHORIZONTALLY:
            return self.ys[4][0]

    def getPath(self, text):
        if text == COPY:
            return self.ys[0][1]
        elif text == REMOVEOBJECT:
            return self.ys[1][1]
        # elif text == UPSIZE:
        #     return self.ys[2][1]
        # elif text == DOWNSIZE:
        #     return self.ys[3][1]
        elif text == RESIZE:
            return self.ys[2][1]
        elif text == FLIPVERTICALLY:
            return self.ys[3][1]
        elif text == FLIPHORIZONTALLY:
            return self.ys[4][1]

    def getCanvas(self):
        return self.canvas

    def selectIcon(self, text):
        if self.scale1 is not None:
            self.scale1.destroy()
            self.scale1 = None
            self.scale2.destroy()
            self.scale2 = None

        x = (WWIDTH - DESKTOPWMAX) / 2
        y = self.getY(text)
        path = self.getPath(text)
        if path.endswith("grey.png"):
            return
        if self.selectedTkId is not None:
            self.rightBar.canvas.delete(self.selectedTkId)

        if self.selectedFunction != text:
            self.selectedFunction = None
            self.selectedTkId = 0
            self.selectedFunction = text
            self.selectedTkId = self.createRectangle(self.rightBar.canvas, x, y, 80, 80)
        else:
            self.selectedFunction = None
            self.selectedTkId = 0

    def unselectIcon(self):
        if self.selectedTkId is not None:
            self.rightBar.canvas.delete(self.selectedTkId)
            self.selectedFunction = None
            self.selectedTkId = 0

    def hoverIcon(self, text):
        x = (WWIDTH - DESKTOPWMAX) / 2
        y = self.getY(text)
        path = self.getPath(text)
        if not path.endswith("grey.png"):
            self.hover = self.createRectangle(self.rightBar.canvas, x, y, 80, 80, "grey")

    def unhoverIcon(self, _):
        self.rightBar.canvas.delete(self.hover)
        self.hover = None

    def removeBorder(self):
        self.parentCanvas.delete(self.borderTkId)

    def drawBorder(self):
        self.removeBorder()
        self.borderTkId = self.parentCanvas.create_rectangle(0, 0, self.canvasWidth, self.canvasHeight,
                                                             outline=PRIMARYCOLOR, width=5)

    def createRectangle(self, canvas, x, y, w, h, color="grey"):
        return canvas.create_rectangle(x - (w / 2), y - (h / 2), x + (w / 2), y + (h / 2), outline=color, width=2)

    def removeBgImage(self):
        self.canvas.delete(self.bgTkId)
        self.bgImage = None
        self.imgObj = None

    def setBgImage(self, img):
        self.canvas.delete(self.bgTkId)
        self.bgImage = img
        self.imgObj = ImageTk.PhotoImage(self.bgImage)
        self.bgTkId = self.canvas.create_image(0, 0, image=self.imgObj, anchor=NW)
        self.canvas.lower(self.bgTkId)

    def saveAs(self, _):
        if len(self.objects) > 0:
            path = asksaveasfile(title=SAVEASEULOHA, initialdir=os.getcwd(), defaultextension=SAVEFILETYPES,
                                 filetypes=SAVEFILETYPES)
            if path:
                dictResult = self.toJson()
                with open(path.name, WRITE) as file:
                    file.write(dictResult)

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

    def addObjectWithImages(self, value, typ, x, y):
        if typ == CLICKABLE and len(value) > CLICKABLEMAX:
            messagebox.showerror(title=ERROR, message=LIMITEXCEEDED)
            return
        else:
            obj = CanvasObject(self, value, typ, x, y)
            self.objects.append(obj)
            return obj

    def lowerBg(self):
        self.canvas.lower(self.bgTkId)

    def setParentCanvasSize(self, width, height):
        self.parentCanvas.config(width=width)
        self.parentCanvas.config(height=height)

    def loadeZosit(self, _):
        result = True
        if len(self.objects) > 0:
            result = messagebox.askyesnocancel(SAVE, WANTSAVE)

            if result:
                self.saveAs(None)

        if result is not None:
            path = askopenfilename(title=CHOOSEEULOHAJSON, initialdir=os.getcwd(), filetypes=SAVEFILETYPES)
            if path and path.endswith(JSONPOSTFIX):
                with open(path, READ) as file:
                    result = json.load(file)

                self.removeAllObjects()
                self.canvas.delete(ALL)
                self.resizeCanvasHeight(result[JSONHEIGHT])
                self.resizeCanvasWidth(result[JSONWIDTH])
                self.setBgColor(result[JSONBGCOLOR])
                self.removeBgImage()

                if result[JSONHOMESVIS]:
                    homeVis = NORMAL
                else:
                    homeVis = HIDDEN

                self.homesVisible = result[JSONHOMESVIS]
                if result[JSONBGIMAGE] is not None:
                    img = textToImage(result[JSONBGIMAGE])
                    self.setBgImage(img)

                self.availButtons = result[JSONAVILBUTT]
                self.loadRightBar()
                self.homes = []
                self.grids = []
                for grid in result[GRIDOBJECTS]:
                    x, y = grid[JSONX], grid[JSONY]
                    gridW, gridH = grid[JSONWIDTH], grid[JSONHEIGHT]
                    color = grid[JSONCOLOR]
                    self.addGrid(x, y, gridW, gridH, color)

                for homeObj in result[HOMEOBJECTS]:
                    self.addHome(homeObj[JSONX], homeObj[JSONY], homeObj[JSONWIDTH], homeObj[JSONHEIGHT], homeVis)

                self.moveRightBar()
                self.setParentCanvasSize(result[JSONWIDTH] + barWidth + 5, WHEIGHT)

                for obj in result[JSONOBJECTS]:
                    if types[obj[JSONTYPE]] == CLONABLE or types[obj[JSONTYPE]] == DRAGGABLE or types[
                        obj[JSONTYPE]] == STATIC:
                        img = textToImage(obj[JSONIMAGE])
                        self.addObjectWithImages(img, types[obj[JSONTYPE]], obj[JSONX], obj[JSONY])
                    elif types[obj[JSONTYPE]] == CLICKABLE:
                        imgs = list()
                        for iimg in obj[JSONIMAGES]:
                            img = textToImage(iimg)
                            imgs.append(img)
                        self.addObjectWithImages(imgs, types[obj[JSONTYPE]], obj[JSONX], obj[JSONY])
                    elif types[obj[JSONTYPE]] == TEXTTYPE:

                        self.addObject(obj[JSONTEXT], types[obj[JSONTYPE]], obj[JSONX], obj[JSONY])
                        textObj = self.objects[-1]
                        textObj.obj.changeWidth(obj[JSONWIDTH])
                        textObj.obj.changeHeight(obj[JSONWIDTH])
                        textObj.obj.setFontSet(obj[JSONFONTUNDER], obj[JSONFONTSTRIKE], obj[JSONFONTWEIGHT],
                                               obj[JSONFONTSLANT], obj[JSONFONTSIZE], obj[JSONFONTFAMILY],
                                               obj[JSONFONTCOLOR])
                        textObj.obj.textEntry.insert(INDEXONE, obj[JSONTEXT])
                        self.text = obj[JSONTEXT]
        for item in self.objects:
            print(item.obj.type)

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
        dictJson[JSONAVILBUTT] = strip_accents_list(self.availButtons)
        dictJson[JSONHOMESVIS] = self.homesVisible

        dictStr = json.dumps(dictJson, indent=4)
        # result = json.loads(dictStr)
        return dictStr
