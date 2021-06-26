import textwrap, math
import threading, queue
from time import sleep
from string import ascii_letters
from PIL import Image, ImageDraw, ImageFont

from timeit import default_timer as timer
from yeskia.baseapp import BaseApp
from yeskia.key import KeyCode
from yeskia.morse import text_to_morse
from yeskia.led import go_beep

class MessageEditor(BaseApp):
    def __init__(self, master, font: ImageFont):
        BaseApp.__init__(self, master)

        self.scroll = 0
        self.font = font
        self.line_height = 1
        self.text = list("HELLO")
        self.statusTexts = ["ABC", str(len(self.text))]
        self.menuText = "Send"
        self.index = len(self.text)
        self.time = 0

        self.isTyping = False
        self.isInitTyping = True
        self.TIMEOUT = 0.6
        self.BLINK_TIMEOUT = 0.5

        self.lastTypeTime = 0
        self.lastBlinkTime = 0
        self.lastKey = -1
        self.cursorVisible = True
        self.isCharMode = True
        self.charRoll = 0
        self.charDict = {
            1: '1', 2: 'ABC2', 3: 'DEF3',
            4: 'GHI4', 5: 'JKL5', 6: 'MNO6',
            7: 'PQRS7', 8: 'TUV8', 9: 'WXYZ9',
            99: '.,/&$()!?_', 0: ' 0'
        }

        self.hold = None
        self.popup = False
        self.q = None


    def update(self, time):
        self.time = time
        self.statusTexts[0] = "ABC" if self.isCharMode else "123"
        self.statusTexts[1] = str(len(self.text))

        if self.q != None and self.q.get():
            self.popup = False
            self.q = None

        d = time - self.lastBlinkTime
        if d > self.BLINK_TIMEOUT:
            if self.isTyping:
                self.cursorVisible = True
            else:
                self.lastBlinkTime = time
                self.cursorVisible = not self.cursorVisible


        if not self.isTyping:
            return

        d = time - self.lastTypeTime
        if d > self.TIMEOUT:
            self.lastTypeTime = time
            self.isTyping = False
            self.index += 1
            self.isInitTyping = True

    def draw(self, draw):
        maxchar, _ = self.getMaxChar()
        wrapped = self.getWrappedText(maxchar)

        y = 0
        for text in wrapped[self.scroll:]:
            draw.text((0, y), text, font=self.font, fill=1, anchor="la")
            y += self.font.getsize(' ')[1] + self.line_height

        self.drawCursor(draw, wrapped, caret=True)

        if self.time == 0:
            self.setScroll()

        if self.popup:
            self.drawPopup(draw)


    def drawCursor(self, draw, wrapped_text, caret=False):
        if not self.cursorVisible:
            return

        w, h = self.font.getsize('r')
        h += self.line_height

        mx = sum(map(len, wrapped_text))
        self.index = min(self.index, mx)

        row, col = self.getCursorPosition(wrapped_text)
        if len(wrapped_text) > 0:
            wth, _ = self.font.getsize(wrapped_text[row][:col])
            row -= self.scroll
        else:
            wth, _ = self.font.getsize('');

        draw.rectangle((wth, row*h+1, wth+w, row*h+h+1), outline=1)

    def drawPopup(self, draw):
        w, h = self.screen_size

        offset = 5
        msg =  'Sending...'
        msgWidth = self.font.getlength(msg)
        w1, _, w2, msgHeight = self.font.getbbox(msg)

        lr = (w - msgWidth) / 2
        tb = (h - msgHeight) /2
        draw.rectangle((lr-offset, tb-offset, w-lr+offset, h-tb+offset), outline=1, fill=1)
        draw.text((lr, tb), msg, font=self.font, fill=0, anchor="la")



    def setScroll(self):
        width, maxline = self.getMaxChar()
        wrapped = self.getWrappedText(width)
        row, _ = self.getCursorPosition(wrapped)

        # scroll down
        if row - self.scroll > maxline:
            self.scroll = row - maxline

        # scroll up
        if row < self.scroll:
            self.scroll = row

    def getWrappedText(self, width):
        text = "".join(self.text)
        wrapped = textwrap.wrap(text, width=width, drop_whitespace=False)
        return wrapped

    def getCursorPosition(self, wrapped_text):
        s, col, row = [0] * 3
        for i, line in enumerate(wrapped_text):
            x = len(line)
            s += x
            if s >= self.index:
                row = i
                col = self.index - (s - x)
                break

        return row, col

    def getMaxChar(self):
        w = self.font.getlength('a')
        h = self.font.getbbox('a')[3] # left, top, right, bottom
        size = self.screen_size

        return int(size[0]/ w), math.floor(size[1]/h) - 1 # idk, must subtract with 1

    def insertChar(self, c, index, inplace=False):
        if inplace:
            if index == len(self.text):
                self.text.append(c)
            else:
                self.text[index] = c
        else:
            front = self.text[:self.index]
            back = self.text[self.index:]
            self.text = front + [c] + back

        self.setScroll()


    # BaseApp event handler
    def onKeyPressed(self, key):
        if self.popup:
            return

        self.isTyping = True
        key = int(key)

        if key == KeyCode.NUM_POUND:
            self.isCharMode = not self.isCharMode
            return

        self.cursorVisible = True

        if self.isCharMode:
            self.typeChar(key)

        else:
            if key < 10:
                c = str(key)
                self.index += 1
                self.insertChar(c, self.index)

            else:
                self.typeChar(key)

        self.lastKey = key

    def typeChar(self, key):
        inplace = False
        d = self.time - self.lastTypeTime

        if self.isInitTyping:
            self.charRoll = 0
            self.isInitTyping = False

        else:
            if d < self.TIMEOUT and self.lastKey == key:
                self.charRoll += 1
                inplace = True
            else:
                self.charRoll = 0
                self.index += 1

        self.lastTypeTime = self.time
        l = len(self.charDict[key])
        c = self.charDict[key][self.charRoll % l]

        self.insertChar(c, self.index, inplace)

    # TODO fast delete on hold
    def onBackPressed(self):
        if self.index == 0:
            return

        del self.text[self.index-1]
        self.index -= 1
        self.setScroll()

    def onNavPressed(self, nav):
        if self.popup:
            return

        self.cursorVisible = True
        self.index = max(0, min(self.index + -nav, len(self.text)))
        self.isTyping = False
        self.isInitTyping = True
        self.setScroll()

    def onMenuPressed(self):
        txt = ''.join(self.text)
        morse = text_to_morse(txt)
        self.popup = True

        self.q = queue.Queue()
        t = threading.Thread(target=go_beep, args=(self.q, morse))
        t.start()
