from PIL import ImageTk, Image


class ImageButton:
    def __init__(self, parent, imgPath, text, x, y, width, height, command):
        self.canvas = parent.getCanvas()
        self.parent = parent
        self.imgPath = imgPath
        self.width = width
        self.height = height
        self.img = Image.open(imgPath)
        self.img = self.img.resize((width, height))
        self.imgObj = ImageTk.PhotoImage(self.img)
        self.x, self.y = x, y
        self.imageTkId = self.canvas.create_image(x, y, image=self.imgObj, anchor='c')
        self.textTkId = self.canvas.create_text(x, y-5, text=text, anchor="c", font=("Times", 20))
        self.canvas.tag_bind(self.textTkId, "<Button-1>", command)
        self.canvas.tag_bind(self.imageTkId, "<Button-1>", command)

    def remove(self):
        self.canvas.delete(self.imageTkId)
        self.canvas.delete(self.textTkId)