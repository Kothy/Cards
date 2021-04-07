import tkinter as tk
from canvases.DesktopCanvas import DesktopCanvas
from canvases.BarCanvas import BarCanvas
from Constants import *
from tkinter.filedialog import asksaveasfile, askopenfilename
from serializeImg import textToImage
import os
import json
import tkinter.ttk as ttk
from screens.AvailableButtonsScreen import AvailableButtonsScreen
from screens.ClickableChangeOrderImagesScreen import ClickableChangeOrderImagesScreen
from screens.CreateGridScreen import CreateGridScreen
from tkinter import messagebox


class ETasksScreen:
    def __init__(self, parent, canvas):
        self.parent = parent
        self.canvas = canvas
        self.windowHeight = WHEIGHT
        self.windowWidth = WWIDTH
        self.canvasHeight = CHEIGHT
        self.canvasWidth = CWIDTH
        self.createRightBar()
        self.createDownBar()
        self.objects = []
        self.menuX, self.menuY = 0, 0
        self.bgImage = None
        self.bgTkId = 0
        self.imgObj = None
        self.itemScale1 = None
        self.itemScale2 = None
        self.availButtons = []
        self.setBinds()
        self.availScreen = AvailableButtonsScreen(self, self.loadAvailableButtons)
        self.changeOrderImagesScreen = ClickableChangeOrderImagesScreen(self, self.windowWidth, self.windowHeight)
        self.createGridScreen = CreateGridScreen(self, self.windowWidth, self.windowHeight, self.hideGridScreen)
        self.desktopCanvas = DesktopCanvas(self, self.canvas, CWIDTH, CHEIGHT)

    def setBinds(self):
        self.canvas.bind_all(BINDMOUSEWHEEL, self.onMouseWheel)

    def onMouseWheel(self, event):
        dx = -2 if event.delta < 0 else 2
        selected = self.desktopCanvas.selected
        if selected is not None and DESKTOPWMAX > selected.getWidth() + dx > 10 and DESKTOPHMAX > selected.getHeight() + dx > 10:
            newW, newH = selected.getWidth() + dx, selected.getHeight() + dx
            selected.changeHeight(newH)
            selected.changeWidth(newW)
            self.itemScale1.set(newW)
            self.itemScale2.set(newH)

    def changeInfoLabelText(self, text):
        self.infoLabel.configure(text=text)

    def createRightBar(self):
        h, w = 40, 40
        self.rightCanvas = BarCanvas(self, self.canvas, WWIDTH - RBARW, 0, RBARBG, RBARW, WHEIGHT)
        self.rightCanvas.addImage(ICOHOME, RBARW / 2, 30, w, h, BACKTOMENU,
                                  self.parent.removeActualScreenAndDisplayMenu, True, anchor=CENTER)
        self.rightCanvas.addImage(ICONEWTASK, RBARW / 2, 90, w, h, NEWEULOHA, self.openNewTask, True, anchor=CENTER)
        self.rightCanvas.addImage(ICOOPENTASK, RBARW / 2, 150, w, h, OPENEULOHA, self.loadeUloha, True, anchor=CENTER)
        self.rightCanvas.addImage(ICOSAVEASULOHA, RBARW / 2, 210, w, h, SAVEULOHA, self.saveUloha, True, anchor=CENTER)

    def createDownBar(self):
        self.downCanvas = BarCanvas(self, self.canvas, 0, WHEIGHT - 44, DOWNBARCOLOR, WWIDTH, 40)
        self.heightScale = tk.IntVar()
        self.widthScale = tk.IntVar()
        self.downCanvas.addScale(WIDTH, self.widthScale, CWIDTH, self.resizeCanvasWidth, 200, DESKTOPWMAX, 0.305, 0.5,
                                 cursor=HORIZARROW, length=WWIDTH / 9.6)
        self.downCanvas.addScale(HEIGHT, self.heightScale, CHEIGHT, self.resizeCanvasHeight, 200, DESKTOPHMAX, 0.415,
                                 0.5, cursor=VERTICARROW, length=WWIDTH / 9.6)
        self.mouseLabel = self.downCanvas.addLabel(CURSORPOSEMPTY, DOWNBARCOLOR, 0.0, 0.5)
        self.canvasLabel = self.downCanvas.addLabel(CANVASSIZE.format(self.canvasWidth, self.canvasHeight),
                                                    DOWNBARCOLOR, 0.08, 0.5)
        self.infoLabel = self.downCanvas.addLabel(OBJECTINFOEMPTY, DOWNBARCOLOR, 0.16, 0.5)
        self.downCanvas.addImage(ICOBUTTONSECONDARY, 0.555, 0.5, int(self.windowWidth / 16), 32, AVAILBUTTONS,
                                 self.showAvailableButtonsScreen,
                                 ratioResize=False, anchor=CENTER, text=True, rel=True)

    def showAvailableButtonsScreen(self, _):
        self.hide()
        self.availScreen.show()

    def showCreateGridScreen(self, obj):
        self.hide()
        self.createGridScreen.object = obj
        self.createGridScreen.show()

    def showchangeOrderImagesScreen(self, object):
        self.hide()
        self.changeOrderImagesScreen.show()
        self.changeOrderImagesScreen.setCommand(self.hidechangeOrderImagesScreen)
        self.changeOrderImagesScreen.showImages(object)

    def hidechangeOrderImagesScreen(self):
        self.show()
        self.changeOrderImagesScreen.hide()

    def hideGridScreen(self, grid, submitted):
        self.show()
        self.createGridScreen.hide()
        if submitted:
            # threading.Thread(target=grid.createGridFromObject).start()
            grid.createGridFromObject()

    def hide(self):
        self.rightCanvas.hide()
        self.downCanvas.hide()
        self.desktopCanvas.hide()
        self.canvas.configure(bg=WHITE)

    def show(self):
        self.canvas.configure(bg=OUTERCANVASBGCOLOR)
        self.downCanvas.show()
        self.rightCanvas.show()
        self.desktopCanvas.show()

    def hideAvailableButtonsScreen(self):
        self.availScreen.hide()
        self.show()

    def loadAvailableButtons(self):
        self.availButtons = []
        self.downCanvas.removeAllImages()
        self.downCanvas.addImage(ICOBUTTONSECONDARY, 0.555, 0.5, int(self.windowWidth / 16), 32, AVAILBUTTONS,
                                 self.showAvailableButtonsScreen,
                                 ratioResize=False, anchor=CENTER, text=True, rel=True)

        self.availScreen.drawButtons(self.availButtons, self.downCanvas)
        self.hideAvailableButtonsScreen()

    def addItemScales(self, w, h, obj, max1=300, max2=300):
        self.itemScale1Var = tk.IntVar()
        self.itemScale2Var = tk.IntVar()
        self.itemScale1Var.set(w)
        self.itemScale2Var.set(h)

        self.itemScale1 = self.downCanvas.addScale(WIDTH, self.itemScale1Var, w,
                                                   lambda e: obj.changeWidth(self.itemScale1Var.get()),
                                                   20, max1, 0.305, 0.5, addToList=False, cursor=HORIZARROW)
        self.itemScale2 = self.downCanvas.addScale(HEIGHT, self.itemScale2Var, h,
                                                   lambda e: obj.changeHeight(self.itemScale2Var.get()),
                                                   20, max2, 0.415, 0.5, addToList=False, cursor=VERTICARROW)

        s = ttk.Style()
        s.configure('My.Horizontal.TScale', background=SECONDARYCOLOR, activebackground=SECONDARYCOLOR)
        self.itemScale1.configure(style='My.Horizontal.TScale')
        self.itemScale2.configure(style='My.Horizontal.TScale')

    def removeItemScales(self):
        if self.itemScale1 is not None:
            self.itemScale1.destroy()

        if self.itemScale2 is not None:
            self.itemScale2.destroy()

        self.itemScale1 = None
        self.itemScale2 = None

    def resizeCanvasHeight(self, _):
        self.desktopCanvas.resizeCanvasHeight(self.heightScale.get())

    def resizeCanvasWidth(self, _):
        self.desktopCanvas.resizeCanvasWidth(self.widthScale.get())

    def getCanvas(self):
        return self.canvas

    def getInnerCanvas(self):
        return self.desktopCanvas

    def getMousePosX(self):
        return self.getCanvas().winfo_pointerx() - self.getCanvas().winfo_rootx()

    def getMousePosY(self):
        return self.getCanvas().winfo_pointery() - self.getCanvas().winfo_rooty()

    def getMousePosXY(self):
        return self.getMousePosX(), self.getMousePosY()

    def remove(self):
        self.canvas.delete(ALL)

    def openNewTask(self, _):
        result = True
        if len(self.desktopCanvas.objects) > 0:
            result = messagebox.askyesnocancel(SAVE, WANTSAVE)

            if result:
                self.saveUloha(None)

        if result is not None:
            self.desktopCanvas.removeAllObjects()

    def loadeUloha(self, _):
        result = True
        if len(self.desktopCanvas.objects) > 0:
            result = messagebox.askyesnocancel(SAVE, WANTSAVE)

            if result:
                self.saveUloha(None)

        if result is not None:
            path = askopenfilename(title=CHOOSEEULOHAJSON, initialdir=os.getcwd(), filetypes=SAVEFILETYPES)
            if path and path.endswith(JSONPOSTFIX):
                with open(path, READ) as file:
                    result = json.load(file)

                self.desktopCanvas.removeAllObjects()
                self.desktopCanvas.resizeCanvasHeight(result[JSONHEIGHT])
                self.desktopCanvas.resizeCanvasWidth(result[JSONWIDTH])
                self.desktopCanvas.setBgColorNoAsk(result[JSONBGCOLOR])
                self.heightScale.set(result[JSONHEIGHT])
                self.widthScale.set(result[JSONHEIGHT])
                self.desktopCanvas.removeBgImage()

                if result[JSONHOMESVIS]:
                    homeVis = NORMAL
                else:
                    homeVis = HIDDEN
                self.desktopCanvas.homesVisible = result[JSONHOMESVIS]
                # self.desktopCanvas.createMenu()

                if result[JSONBGIMAGE] is not None:
                    img = textToImage(result[JSONBGIMAGE])
                    self.desktopCanvas.setBgImageNoAsk(img)

                self.downCanvas.removeAllImages()
                self.downCanvas.addImage(ICOBUTTONSECONDARY, 0.555, 0.5, int(self.windowWidth / 16), 32, AVAILBUTTONS,
                                         self.showAvailableButtonsScreen,
                                         ratioResize=False, anchor=CENTER, text=True, rel=True)

                self.availButtons = result[JSONAVILBUTT]
                self.availScreen.drawButtonsWithArray(self.availButtons, self.downCanvas)
                self.desktopCanvas.homes = []
                self.desktopCanvas.grids = []
                for grid in result[GRIDOBJECTS]:
                    x, y = grid[JSONX], grid[JSONY]
                    gridW, gridH = grid[JSONWIDTH], grid[JSONHEIGHT]
                    color = grid[JSONCOLOR]
                    self.desktopCanvas.addGrid(x, y, gridW, gridH, color)

                for homeObj in result[HOMEOBJECTS]:
                    self.desktopCanvas.addHome(homeObj[JSONX], homeObj[JSONY], homeObj[JSONWIDTH], homeObj[JSONHEIGHT],
                                               homeVis)

                for obj in result[JSONOBJECTS]:
                    if types[obj[JSONTYPE]] == CLONABLE or types[obj[JSONTYPE]] == DRAGGABLE or types[
                        obj[JSONTYPE]] == STATIC:
                        img = textToImage(obj[JSONIMAGE])
                        self.desktopCanvas.addObjectWithImages(img, types[obj[JSONTYPE]], obj[JSONX], obj[JSONY])
                    elif types[obj[JSONTYPE]] == CLICKABLE:
                        imgs = list()
                        for iimg in obj[JSONIMAGES]:
                            img = textToImage(iimg)
                            imgs.append(img)
                        self.desktopCanvas.addObjectWithImages(imgs, types[obj[JSONTYPE]], obj[JSONX], obj[JSONY])
                    elif types[obj[JSONTYPE]] == TEXTTYPE:

                        self.desktopCanvas.addObject(obj[JSONTEXT], types[obj[JSONTYPE]], obj[JSONX], obj[JSONY])
                        textObj = self.desktopCanvas.objects[-1]
                        textObj.obj.changeWidth(obj[JSONWIDTH])
                        textObj.obj.changeHeight(obj[JSONWIDTH])
                        textObj.obj.setFontSet(obj[JSONFONTUNDER], obj[JSONFONTSTRIKE], obj[JSONFONTWEIGHT],
                                               obj[JSONFONTSLANT], obj[JSONFONTSIZE], obj[JSONFONTFAMILY],
                                               obj[JSONFONTCOLOR])
                        textObj.obj.textEntry.insert(INDEXONE, obj[JSONTEXT])
                        self.text = obj[JSONTEXT]

    def saveUloha(self, _):
        path = asksaveasfile(title=SAVEASEULOHA, initialdir=os.getcwd(), defaultextension=SAVEFILETYPES,
                             filetypes=SAVEFILETYPES)
        if path:
            result, dictResult = self.desktopCanvas.toJson()
            with open(path.name, WRITE) as file:
                file.write(dictResult)
