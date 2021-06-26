import textwrap, math
from PIL import Image, ImageDraw, ImageFont

from yeskia.baseapp import BaseApp

class Shape(BaseApp):
    def __init__(self, master):
        BaseApp.__init__(self, master)

    def draw(self, draw: ImageDraw):
        draw.rectangle([0, 0, 80, 44], outline=1)
