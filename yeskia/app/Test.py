from yeskia.key import NavKey
from yeskia.baseapp import BaseApp
from yeskia.music.AddNumber import AddNumber

class TestApp(BaseApp):
    def __init__(self, master, font):
        self.font = font
        BaseApp.__init__(self, master)
        self.number = 14112

    def draw(self, draw):
        draw.text((0, 0), str(self.number), font=self.font, fill=1)
        draw.rectangle((20, 20, 80, 40), outline=1)

    def onMenuPressed(self, prevent=None):
        self.number += 1
