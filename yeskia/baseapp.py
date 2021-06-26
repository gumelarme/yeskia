from PIL import ImageDraw, ImageFont
from typing import Callable, Tuple
from yeskia.key import KeyCode, NavKey

class BaseApp:
    def __init__(self, master):
        self.master = master
        self.statusTexts = []
        self.menuText = "Menu"
        self.__screen_size = (0, 0)

    def draw(self, draw: ImageDraw) -> None:
        pass

    @property
    def screen_size(self) -> Tuple[int, int]:
        return self.__screen_size;

    @screen_size.setter
    def screen_size(self, size: Tuple[int, int]):
        self.__screen_size = size


    def update(self, time):
        pass

    def onKeyPressed(self, key: KeyCode) -> None:
        pass

    def onMenuPressed(self, prevent: Callable=None) -> None:
        pass

    def onBackPressed(self, prevent: Callable=None) -> None:
        pass

    def onNavPressed(self, nav: NavKey, prevent: Callable=None) -> None:
        pass
