import board
from time import sleep
from digitalio import DigitalInOut, Direction

buzz = DigitalInOut(board.D21)
buzz.direction = Direction.OUTPUT

led = DigitalInOut(board.D20)
led.direction = Direction.OUTPUT

TIME = 0.05

def dash():
    led.value = True
    buzz.value = True

    sleep(TIME * 3)

    led.value = False
    buzz.value = False

def dot():
    led.value = True
    buzz.value = True

    sleep(TIME)

    led.value = False
    buzz.value = False

def go_beep(queue, morse):
    for word in morse:
        for letter in word:
            for x in letter:
                if x == '1':
                    dash()
                else:
                    dot()

                sleep(TIME)
            sleep(TIME * 3)
        sleep(TIME * 7)
    queue.put(True)
