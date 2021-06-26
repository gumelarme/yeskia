class Core:
    def __init__(self, applist, font, statusFont):
        self.__applist = applist
        self.font = font
        self.statusFont = statusFont
        self.__active_app = 0

    @property
    def app(self):
        return self.__applist[self.__active_app]
