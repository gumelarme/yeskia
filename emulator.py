import tkinter as tk
from time import sleep
from timeit import default_timer

from PIL import ImageFont

from yeskia.key import NavKey, KeyCode
from yeskia.painter import TkinterCanvasPainter
from yeskia.app.message_editor import MessageEditor
from yeskia.data import MainData
from yeskia.core import Core


FACTOR = 3
FONTSIZE = 8
STATUS_FONTSIZE = 5
FONTFACE = "./fonts/FiraCode-Regular.ttf"
class Emulator(Core, tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__init_props()
        self.parent = parent

        font = ImageFont.truetype(FONTFACE, FONTSIZE*FACTOR)
        statusFont = ImageFont.truetype(FONTFACE, STATUS_FONTSIZE*FACTOR)
        applist = [
            MessageEditor(self, font),
        ]

        Core.__init__(self, applist, font, statusFont)

        self.painter = TkinterCanvasPainter(self, width=84*FACTOR, height=48*FACTOR)
        self.painter.pack()

        self.control = Control(self)
        self.control.pack()
        self.loop()

    def __init_props(self):
        self.quitApp = False
        self.data = MainData()
        self.render_font = ImageFont.truetype(self.data.fontpath, 10*FACTOR)


    def loop(self):
        sleep(1/30)
        self.after(1, self.painter.paint)
        self.after(1, lambda: self.app.update(default_timer()))
        self.after(1, self.loop)


    def onQuit(self):
        print("Render process stopped, quitting...")
        self.parent.destroy()


class Control(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        sv = tk.StringVar()
        sv.trace("w", lambda name, i, mode, sv=sv: self.textInput_onChange(sv))
        # Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)
        self.columnconfigure(2, pad=10)
        self.columnconfigure(3, pad=10)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)
        self.rowconfigure(3, pad=10)
        self.rowconfigure(4, pad=10)

        self.btn1 = tk.Button(self, text="1", command=lambda: self.btnPress(KeyCode.NUM_1))
        self.btn2 = tk.Button(self, text="2", command=lambda: self.btnPress(KeyCode.NUM_2))
        self.btn3 = tk.Button(self, text="3", command=lambda: self.btnPress(KeyCode.NUM_3))
        self.btn4 = tk.Button(self, text="4", command=lambda: self.btnPress(KeyCode.NUM_4))
        self.btn5 = tk.Button(self, text="5", command=lambda: self.btnPress(KeyCode.NUM_5))
        self.btn6 = tk.Button(self, text="6", command=lambda: self.btnPress(KeyCode.NUM_6))
        self.btn7 = tk.Button(self, text="7", command=lambda: self.btnPress(KeyCode.NUM_7))
        self.btn8 = tk.Button(self, text="8", command=lambda: self.btnPress(KeyCode.NUM_8))
        self.btn9 = tk.Button(self, text="9", command=lambda: self.btnPress(KeyCode.NUM_9))
        self.btn0 = tk.Button(self, text="0", command=lambda: self.btnPress(KeyCode.NUM_0))
        self.btnStar = tk.Button(self, text="*", command=lambda: self.btnPress(KeyCode.NUM_STAR))
        self.btnPound = tk.Button(self, text="#", command=lambda: self.btnPress(KeyCode.NUM_POUND))

        self.btnUp = tk.Button(self, text="UP", command=self.btnUp)
        self.btnDown = tk.Button(self, text="Down", command=self.btnDown)
        self.btnDel = tk.Button(self, text="DEL", command=self.btnDelete)
        self.btnMenu = tk.Button(self, text="MENU", command=self.btnMenu)

        self.btn1.grid(row=1, column=0)
        self.btn2.grid(row=1, column=1)
        self.btn3.grid(row=1, column=2)
        self.btn4.grid(row=2, column=0)
        self.btn5.grid(row=2, column=1)
        self.btn6.grid(row=2, column=2)
        self.btn7.grid(row=3, column=0)
        self.btn8.grid(row=3, column=1)
        self.btn9.grid(row=3, column=2)

        self.btnStar.grid(row=4, column=0)
        self.btn0.grid(row=4, column=1)
        self.btnPound.grid(row=4, column=2)

        self.btnUp.grid(row=0, column=0)
        self.btnDown.grid(row=0, column=2)
        self.btnDel.grid(row=0, column=3)
        self.btnMenu.grid(row=0, column=1)

    def btnPress(self, val):
        self.parent.app.onKeyPressed(val)

    def btnDelete(self):
        self.parent.app.onBackPressed()

    def btnUp(self):
        self.parent.app.onNavPressed(NavKey.UP)

    def btnDown(self):
        self.parent.app.onNavPressed(NavKey.DOWN)

    def btnMenu(self):
        self.parent.app.onMenuPressed()


if __name__ == '__main__':
    root = tk.Tk()

    emulator = Emulator(root)
    emulator.pack(side="top", fill="both", expand=True)

    root.attributes('-type', 'dialog')
    root.protocol("WM_DELETE_WINDOW", emulator.onQuit)
    root.mainloop()
