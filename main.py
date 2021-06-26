import adafruit_matrixkeypad
import board
import digitalio as dio
import time

from PIL import ImageFont

from yeskia.viewport import Viewport
from yeskia.core import Core
from yeskia.app.message_editor import MessageEditor
from yeskia.app.shape import Shape
from yeskia.key import NavKey

FONTSIZE = 10
STATUS_FONTSIZE = 8
FONTFACE = "./fonts/FiraCode-Regular.ttf"
COL_PIN = [board.D2, board.D3, board.D4, board.D17]
ROW_PIN = [board.D27, board.D22, board.D23, board.D24]

class Main(Core):
    def __init__(self):
        font = ImageFont.truetype(FONTFACE, FONTSIZE)
        statusFont = ImageFont.truetype(FONTFACE, STATUS_FONTSIZE)
        applist = [
            MessageEditor(self, font),
        ]

        Core.__init__(self, applist, font, statusFont)

        self.init_keys()
        self.viewport = Viewport(self)
        self.viewport.before(self.check_button_pressed)

    def init_keys(self):
        keys = ((1, 2, 3, 'A'),
                (4, 5, 6, 'B'),
                (7, 8, 9, 'C'),
                ('*', 0, '#', 'D'))

        rows = [dio.DigitalInOut(x) for x in COL_PIN]
        cols = [dio.DigitalInOut(x) for x in ROW_PIN]
        self.keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

    def check_button_pressed(self):
        if hasattr(self, 'keypad'):
            self.init_keys()

        keys = self.keypad.pressed_keys
        if keys:
            k = keys[0]
            if k in range(10):
                self.app.onKeyPressed(int(k))

            elif k == '*':
                self.app.onKeyPressed(99)

            elif k == '#':
                self.app.onKeyPressed(98)

            elif k == 'A':
                self.app.onNavPressed(NavKey.UP)

            elif k == 'B':
                self.app.onNavPressed(NavKey.DOWN)

            elif k == 'C':
                self.app.onBackPressed()

            elif k == 'D':
                self.app.onMenuPressed()

            time.sleep(.1)

    def run(self):
        self.viewport.mainloop()

if __name__ == '__main__':
    main = Main()
    main.run()
