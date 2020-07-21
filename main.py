# Nelson's Desktop Switcher with Scroll
#
#
#
#
## Import the libraries
import time
import board
import rotaryio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse
import usb_hid

## define output LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

## flash the LED at boot
for x in range(0, 9):
    led.value = False
    time.sleep(0.05)
    led.value = True
    time.sleep(0.05)

## configure device as keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

## configure mouse for scroll function
m = Mouse(usb_hid.devices)

## define buttons
encClick = DigitalInOut(board.D9)
encClick.direction = Direction.INPUT
encClick.pull = Pull.UP

b1 = DigitalInOut(board.D0)
b1.direction = Direction.INPUT
b1.pull = Pull.UP

b2 = DigitalInOut(board.D3)
b2.direction = Direction.INPUT
b2.pull = Pull.UP

b3 = DigitalInOut(board.D6)
b3.direction = Direction.INPUT
b3.pull = Pull.UP

## define encoder
encoder = rotaryio.IncrementalEncoder(board.D8, board.D7)
last_position = 0
osChoice = 0

## blink / debouncer
def bD(x):
    for i in range(0, x):
        led.value = False
        time.sleep(0.05)
        led.value = True
        time.sleep(0.05)

## loop 
while True:
    ## choose OS
    if not b1.value:
        bD(1)
        osChoice = 0
        time.sleep(0.1)
    if not b2.value:
        bD(2)
        osChoice = 1
        time.sleep(0.1)
    if not b3.value:
        bD(3)
        osChoice = 2
        time.sleep(0.1)
        
    position = encoder.position

    ## mouse scroll when pressed
    if not encClick.value:
        if position < last_position:
            m.move(wheel=1)
            bD(1)
            last_position = position
        if position > last_position:
            m.move(wheel=-1)
            bD(1)
            last_position = position
            
    ## main desktop switcher loop
    if osChoice == 0 and encClick.value:
        if position < last_position:
            kbd.send(Keycode.GUI, Keycode.CONTROL, Keycode.LEFT_ARROW)
            bD(1)
            last_position = position
        if position > last_position:
            kbd.send(Keycode.GUI, Keycode.CONTROL, Keycode.RIGHT_ARROW)
            bD(1)
            last_position = position
    if osChoice == 1 and encClick.value:
        if position < last_position:
            kbd.send(Keycode.CONTROL, Keycode.LEFT_ARROW)
            bD(1)
            last_position = position
        if position > last_position:
            kbd.send(Keycode.CONTROL, Keycode.RIGHT_ARROW)
            bD(1)
            last_position = position
    if osChoice == 2 and encClick.value:
        if  position < last_position:
            kbd.send(Keycode.GUI, Keycode.CONTROL, Keycode.UP_ARROW)
            bD(1)
            last_position = position
        if position > last_position:
            kbd.send(Keycode.GUI, Keycode.CONTROL, Keycode.DOWN_ARROW)
            bD(1)
            last_position = position

