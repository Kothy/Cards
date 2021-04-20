import tkinter as tk
from ImageButton import ImageButton
from PIL import ImageTk, Image
from screens.ETasksScreen import ETasksScreen
from screens.eZositScreen import eZositScreen
from Constants import *
from ttkthemes import ThemedTk


class Main:
    def __init__(self):
        self.windowHeight = WHEIGHT
        self.windowWidth = WWIDTH
        self.buttons = []
        self.canvasInit()
        self.actualScreen = None
        self.bgTkId = 0
        # self.displayMenuScreen()
        self.displayETasksScreen(None)
        # self.displayeZositScreen(None)
        self.root.mainloop()

    def setBackground(self):
        self.imgBg = Image.open("images/backgrounds/bg7.jpg")
        self.imgBg = self.imgBg.resize((self.windowWidth, self.windowHeight))
        self.imgBgObj = ImageTk.PhotoImage(self.imgBg)
        self.bgTkId = self.canvas.create_image(0, 0, image=self.imgBgObj, anchor='nw')

    def canvasInit(self):
        self.root = ThemedTk(theme="yaru")
        # print(self.root.themes)
        self.root.title("Karticky")
        self.root.state('zoomed')
        self.root.resizable(False, True)
        self.canvas = tk.Canvas(self.root, width=self.windowWidth, height=self.windowHeight,
                                bg=OUTERCANVASBGCOLOR, highlightthickness=0)
        self.canvas.pack(expand=tk.NO)

    def displayETasksScreen(self, _):
        self.removeActualScreen()
        self.actualScreen = ETasksScreen(self, self.canvas)

    def displayeZositScreen(self, _):
        self.removeActualScreen()
        self.actualScreen = eZositScreen(self.canvas)

    def removeMenu(self):
        self.canvas.delete(self.bgTkId)
        for button in self.buttons:
            button.remove()

    def removeActualScreen(self):
        if self.actualScreen is None:
            self.removeMenu()
        else:
            self.actualScreen.remove()
            self.actualScreen = None

    def removeActualScreenAndDisplayMenu(self, e=None):
        self.removeActualScreen()
        self.displayMenuScreen()

    def getCanvas(self):
        return self.canvas

    def displayMenuScreen(self):
        self.setBackground()
        self.buttons = []
        button = ImageButton(self, ICOBUTTONSECONDARY, "eZošit", self.windowWidth / 2, 400, 400, 80,
                             self.displayeZositScreen)
        button2 = ImageButton(self, ICOBUTTONSECONDARY, "eÚlohy", self.windowWidth / 2, 550, 400, 80,
                              self.displayETasksScreen)

        self.buttons.append(button)
        self.buttons.append(button2)


Main()
