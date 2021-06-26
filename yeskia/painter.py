import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageOps
from yeskia.core import Core

class Painter:
    def __init__(self, core, width, height):
        self.offset = 1
        self.core = core
        self.width = width
        self.height = height

    def clear(self):
        pass

    def get_blank(self):
        bg = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(bg)
        return bg, draw

    def paintStatus(self, draw):
        x = 0
        height = self.core.statusFont.getsize(' ')[1]
        for text in self.core.app.statusTexts:
            draw.text((x, 0), text, font=self.core.statusFont, fill=1, anchor="la")
            x = self.core.statusFont.getsize(text + ' ')[0]

        return height

    def paintMenu(self, draw):
        font, text = self.core.statusFont, self.core.app.menuText
        w, h = font.getsize(text)

        y = self.height - h
        x = (self.width - w) / 2

        draw.text((x, y), text, font=font, fill=1)
        return h + self.offset


    def paint(self):
        bg, draw = self.get_blank()
        #drawing application
        h1 = self.paintStatus(draw)
        h2 = self.paintMenu(draw)

        appImage, appDraw = self.getAppImageDraw(h1 + h2)
        self.core.app.screen_size = (self.width, self.height - (h1 + h2))
        self.core.app.draw(appDraw)

        bg.paste(appImage, (self.offset, h1))
        self.display(bg)

    def invert(self, image):
        return ImageOps.invert(image.convert('RGB')).convert('1')

    def getAppImageDraw(self, h):
        size = tuple(x - self.offset for x in (self.width, self.height - h))
        img = Image.new("1", size)
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, size[0], size[1]), fill=0)

        return img, draw

    """
    User implemented function to put the image in the screen,
    called by the draw method.
    """
    def display(self, image):
        pass


class NokiaScreenPainter(Painter):
    def __init__(self, core, display):
        Painter.__init__(self, core, display.width, display.height)
        self.screen = display

    def clear(self):
        self.screen.fill(0)
        self.screen.show()

    def display(self, image):
        self.screen.image(image)
        self.screen.show()

class TkinterCanvasPainter(tk.Frame, Painter):
    def __init__(self, core, *args, **kwargs):
        tk.Frame.__init__(self, core, *args, **kwargs)
        self.core = core

        width = kwargs['width'] if 'width' in kwargs else 0
        height = kwargs['height'] if 'height' in kwargs else 0


        Painter.__init__(self, self.core, width, height)
        canvas = tk.Canvas(self.core, width=self.width, height=self.height)
        canvas.pack()
        self.canvas = canvas
        self.offset = 5

    def display(self, image):

        image = self.invert(image)
        imgtk = ImageTk.PhotoImage(image)
        self.image_holder = imgtk
        sprite = self.canvas.create_image(self.width/2, self.height/2, image=imgtk)
