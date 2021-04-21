from tkinter import font
import tkinter as tk
from Constants import *
from tkfontchooser import askfont
import copy
from tkinter import colorchooser


class TextObject:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.textEntry = None
        self.text = EMPTYSTRING
        self.tkId = 0
        self.tkSelectId = 0
        self.type = TEXTTYPE
        self.menuX = 0
        self.menuY = 0
        self.height = TEHEIGHT
        self.width = TEWIDTH
        self.fontSet = {
            UNDERLINE: False,
            OVERSTRIKE: False,
            WEIGHT: NORMAL,
            SLANT: ROMAN,
            SIZE: 20,
            FAMILY: DEFAULTFONT,
            COLOR: BLACK
        }
        self.bgColor = PRIMARYCOLOR
        self.gridBorder = []
        self.font = font.Font()
        self.font.configure(family=DEFAULTFONT)
        self.font.configure(size=20)
        self.createTextEntry()
        self.createMenu()

    def displayMenu(self, event):
        self.menuX, self.menuY = event.x_root, event.y_root
        self.menu.tk_popup(event.x_root, event.y_root, 0)

    def createMenu(self):
        self.menu = tk.Menu(self.getCanvas(), tearoff=0, selectcolor=RED)
        self.menu.add_command(label=CHANGEFONT, command=self.changeFont)
        self.menu.add_command(label=CHANGEFONTCOLOR, command=self.changeFontColor)
        self.menu.add_command(label=CHANGEBGCOLOR, command=self.changeBgColor)
        self.menu.add_separator()
        text = DESELECT if self.parent.selected else SELECT
        self.menu.add_command(label=text, command=self.toggle)
        self.menu.add_command(label=COPY, command=self.copy)
        self.menu.add_command(label=REMOVEOBJECT, command=self.remove)
        self.menu.add_separator()
        self.menu.add_command(label=CREATEGRID, command=self.createGrid)

    def createGrid(self):
        self.parent.parent.parent.showCreateGridScreen(self)

    def setFontSet(self, underli, overst, weight, slant, size, family, color):
        myFont = font.Font(self.textEntry, self.textEntry.cget(FONTTEXT))
        self.fontSet[UNDERLINE] = underli
        self.fontSet[OVERSTRIKE] = overst
        self.fontSet[WEIGHT] = weight
        self.fontSet[SLANT] = slant
        self.fontSet[SIZE] = size
        self.fontSet[FAMILY] = family
        self.fontSet[COLOR] = color
        myFont.configure(underline=underli)
        myFont.configure(overstrike=overst)
        myFont.configure(weight=weight)
        myFont.configure(slant=slant)
        myFont.configure(size=size)
        myFont.configure(family=family)
        if len(self.fontSet[FAMILY]) > 15:
            self.fontSet[FAMILY] = self.fontSet[FAMILY][0:15] + DOTDOTDOT
        self.textEntry.configure(font=myFont)
        self.textEntry.configure(fg=color)

    def changeFont(self):
        fontDict = askfont(title=CHOOSEFONT)
        if fontDict:
            myFont = font.Font(self.textEntry, self.textEntry.cget(FONTTEXT))
            underli = True if fontDict[UNDERLINE] == 1 else False
            overstri = True if fontDict[OVERSTRIKE] == 1 else False
            myFont.configure(underline=underli)
            myFont.configure(overstrike=overstri)
            myFont.configure(weight=fontDict[WEIGHT])
            myFont.configure(slant=fontDict[SLANT])
            myFont.configure(size=int(fontDict[SIZE]))
            myFont.configure(family=(fontDict[FAMILY]))
            self.font = myFont
            self.fontFamily = fontDict[FAMILY]
            self.fontSet[UNDERLINE] = underli
            self.fontSet[OVERSTRIKE] = overstri
            self.fontSet[WEIGHT] = fontDict[WEIGHT]
            self.fontSet[SLANT] = fontDict[SLANT]
            self.fontSet[SIZE] = int(fontDict[SIZE])
            self.fontSet[FAMILY] = fontDict[FAMILY]
            if len(self.fontSet[FAMILY]) > 15:
                self.fontSet[FAMILY] = self.fontSet[FAMILY][0:15] + DOTDOTDOT
            self.textEntry.configure(font=myFont)

    def changeWidth(self, value):
        self.text = self.textEntry.get(INDEXONE, tk.END)
        self.width = value
        if self.parent.selected:
            self.drawBorder()
        self.inner.place(width=self.width, height=self.height, x=self.x, y=self.y, anchor=CENTER)

    def changeHeight(self, value):
        self.text = self.textEntry.get(INDEXONE, tk.END)
        self.height = value
        if self.parent.selected:
            self.drawBorder()
        self.inner.place(width=self.width, height=self.height, x=self.x, y=self.y, anchor=CENTER)

    def changeFontColor(self):
        color = colorchooser.askcolor(title=CHOOSECOLOR, color=self.fontSet[COLOR])
        if color != (None, None):
            color = color[1]
            self.fontSet[COLOR] = color
            self.textEntry.configure(fg=color)

    def changeBgColor(self):
        color = colorchooser.askcolor(title=CHOOSECOLOR, color=self.bgColor)
        if color != (None, None):
            color = color[1]
            self.bgColor = color
            self.textEntry.configure(bg=color)

    def changeBgColorNoAsk(self, color):
        self.bgColor = color
        self.textEntry.configure(bg=color)

    def getText(self):
        return self.textEntry.get(INDEXONE, tk.END)

    def createTextEntry(self):
        self.getCanvas().update()
        self.getCanvas().delete(self.tkId)
        self.inner = tk.Canvas(self.getCanvas(), bd=2)
        self.textEntry = tk.Text(self.inner, background=self.bgColor, foreground=self.fontSet[COLOR],
                                 width=self.width, font=self.font, height=self.height, padx=8, pady=5, relief=tk.RIDGE)

        self.textEntry.insert(INDEXONE, self.text)
        self.textEntry.pack()
        self.textEntry.bind(BINDRIGHTMOTION, self.dragDrop)
        self.textEntry.bind(BINDRIGHTBUTT, self.displayMenu)
        self.textEntry.bind(BINDLEFTRELEASE, self.onRelease)

        self.textEntry.bind(BINDENTER, self.displayInfo)
        self.textEntry.bind(BINDLEAVE, self.hideInfo)
        self.textEntry.bind(BINDRIGHTBUTT, self.displayMenu)
        self.inner.pack()
        self.tkId = self.getCanvas().create_window(self.x, self.y, window=self.inner,
                                                   width=self.width, height=self.height, anchor=CENTER)
        if self.parent.selected:
            self.getCanvas().delete(self.tkSelectId)
            self.tkSelectId = self.getCanvas().create_rectangle(self.x - (self.width / 2),
                                                                self.y - (self.height / 2), self.x + (self.width / 2),
                                                                self.y + (self.height / 2), width=2)
        self.getCanvas().update()

    def onRelease(self, _):
        self.textEntry.configure(selectbackground=SYSTEMHIGHLIGHT, inactiveselectbackground=SYSTEMHIGHLIGHT)

    def copy(self, x=None, y=None):
        newX = self.x + 30 if x is None else x
        newY = self.y + 30 if y is None else y
        newObject = self.parent.parent.addObject(EMPTYSTRING, self.type, newX, newY)
        newObject = newObject.getObject()
        newObject.text = self.getText()
        newObject.height = copy.copy(self.height)
        newObject.width = copy.copy(self.width)
        newObject.fontColor = copy.copy(self.fontSet[COLOR])
        newObject.fontSize = copy.copy(self.fontSet[SIZE])
        newObject.fontFamily = copy.copy(self.fontSet[FAMILY])
        newObject.bgColor = copy.copy(self.bgColor)
        newObject.font = font.Font()
        newObject.font.configure(family=newObject.fontFamily)
        newObject.font.configure(size=newObject.fontSize)
        newObject.createTextEntry()

    def hide(self):
        self.getCanvas().itemconfig(self.tkId, state=HIDDEN)

    def show(self):
        self.getCanvas().itemconfig(self.tkId, state=NORMAL)

    def getMain(self):
        return self.parent.parent.parent

    def displayInfo(self, _):
        self.getMain().changeInfoLabelText(OBJECTINFO.format("Písmo: {}, Veľkosť: {}"
                                                             .format(self.fontSet[FAMILY], self.fontSet[SIZE])))

    def hideInfo(self, _):
        self.getMain().changeInfoLabelText(OBJECTINFOEMPTY)

    def toggle(self):
        if not self.parent.selected:
            self.select()
            self.getMain().addItemScales(self.width, self.height, self, self.getMain().canvasWidth, 400)
        else:
            self.getMain().removeItemScales()
            self.unselect()
        self.createMenu()

    def destroy(self):
        self.textEntry.destroy()
        self.inner.destroy()
        self.getCanvas().delete(self.tkId)
        self.getCanvas().delete(self.tkSelectId)

    def dragDrop(self, event):
        self.text = self.textEntry.get(INDEXONE, tk.END)
        self.textEntry.configure(selectbackground=self.bgColor, inactiveselectbackground=self.bgColor)
        self.textEntry.tag_remove(tk.SEL, INDEXONE, tk.END)
        x = self.parent.getMousePosX()
        y = self.parent.getMousePosY()
        self.setX(x)
        self.setY(y)
        self.inner.place(width=self.width, height=self.height, x=self.x, y=self.y, anchor=CENTER)
        if self.parent.selected:
            self.drawBorder()

    def remove(self):
        self.destroy()
        self.parent.remove()

    def select(self):
        self.parent.parent.unselectAll()
        self.parent.selected = True
        self.parent.parent.selected = self.parent
        self.drawBorder()

    def drawBorder(self):
        self.getCanvas().delete(self.tkSelectId)
        self.tkSelectId = self.getCanvas().create_rectangle(self.x - (self.width / 2), self.y - (self.height / 2),
                                                            self.x + (self.width / 2),
                                                            self.y + (self.height / 2), width=3)

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

    def toJson(self):
        obj = dict()
        obj[JSONX] = self.x
        obj[JSONY] = self.y
        obj[JSONTYPE] = types[self.type]
        obj[JSONWIDTH] = self.width
        obj[JSONHEIGHT] = self.height
        obj[JSONTEXT] = self.getText()
        obj[JSONFONTCOLOR] = self.fontSet[COLOR]
        obj[JSONFONTSIZE] = self.fontSet[SIZE]
        obj[JSONFONTFAMILY] = self.fontSet[FAMILY]
        obj[JSONFONTUNDER] = self.fontSet[UNDERLINE]
        obj[JSONFONTSTRIKE] = self.fontSet[OVERSTRIKE]
        obj[JSONFONTWEIGHT] = self.fontSet[WEIGHT]
        obj[JSONFONTSLANT] = self.fontSet[SLANT]
        obj[JSONBGCOLOR] = self.bgColor
        return obj
