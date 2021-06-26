from time import sleep
from typing import Callable, List
from timeit import default_timer

import adafruit_pcd8544
import board
import busio
import digitalio

from yeskia.painter import NokiaScreenPainter

class Viewport:
    def __init__(self, core):
        self.core = core
        self.beforeQueue: List[Callable] = []
        self.afterQueue: List[Callable]= []
        self.isQuit = False

        self.display, self.backlight = self.getDisplay()
        self.clearDisplay()

        self.painter = NokiaScreenPainter(core, self.display)

    def mainloop(self):
        fps = 30
        try:
            last_time = default_timer()
            while not self.isQuit:
                time = default_timer()
                d =  time - last_time

                if d < 1/fps:
                    continue


                self.runBefore()
                self.painter.paint()
                self.core.app.update(time)
                self.runAfter()
                last_time = time
        finally:
            self.isQuit = True
            print("Ending main loop")

    def runBefore(self):
        for func in self.beforeQueue:
            func()

    def runAfter(self):
        for func in self.afterQueue:
            func()

    def before(self, func: Callable):
        self.beforeQueue.append(func)

    def after(self, func: Callable):
        self.afterQueue.append(func)

    def getDisplay(self):
        # TODO: customization
        spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        dc = digitalio.DigitalInOut(board.D6)  # data/command
        cs = digitalio.DigitalInOut(board.CE0)  # Chip select
        reset = digitalio.DigitalInOut(board.D5)  # reset

        display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)

        # Contrast and Brightness Settings
        display.bias = 4
        display.contrast = 50

        backlight = digitalio.DigitalInOut(board.D13)
        backlight.switch_to_output()
        backlight.value = False

        return display, backlight

    def clearDisplay(self):
        self.display.fill(0)
        self.display.show()

    def toggleBacklight(self):
        self.backlight.value = not self.backlight.value
