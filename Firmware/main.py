import time
import math
import board
import busio
import neopixel

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler


# ============================================================
# GLITCHPAD
# ============================================================

keyboard = KMKKeyboard()


# ============================================================
# BUTTONS — DIRECT GPIO
#
# Each switch:
# GPIO ---- SWITCH ---- GND
#
# D0 = UP
# D1 = DOWN
# D2 = LEFT
# D3 = RIGHT
# D6 = SHIFT
# D7 = SPACE
# ============================================================

BUTTON_PINS = [
board.D0, # UP
board.D1, # DOWN
board.D2, # LEFT
board.D3, # RIGHT
board.D6, # SHIFT
board.D7, # SPACE
]

keyboard.matrix = KeysScanner(
pins=BUTTON_PINS,
value_when_pressed=False,
pull=True,
)

keyboard.keymap = [
[
KC.UP,
KC.DOWN,
KC.LEFT,
KC.RIGHT,
KC.LSFT,
KC.SPC,
]
]


# ============================================================
# ROTARY ENCODER
#
# D8 = A
# D9 = B
# C = GND
#
# Rotation selects number slots 1-9.
# ============================================================

encoder_handler = EncoderHandler()

encoder_handler.pins = (
(board.D8, board.D9, None, True),
)

encoder_handler.map = [
(
(KC.N1, KC.N2),
),
]

keyboard.modules.append(encoder_handler)


# ============================================================
# OLED
#
# D4 = SDA
# D5 = SCL
#
# 128 x 32 I2C OLED
# ============================================================

import adafruit_ssd1306

i2c = busio.I2C(
board.D5,
board.D4,
)

oled = adafruit_ssd1306.SSD1306_I2C(
128,
32,
i2c,
addr=0x3C,
)


# ============================================================
# SK6812 MINI-E
#
# D10 = LED1 DIN
# 20 LEDs total
# ============================================================

LED_COUNT = 20

pixels = neopixel.NeoPixel(
board.D10,
LED_COUNT,
brightness=0.15,
auto_write=False,
)


# ============================================================
# RGB — CYBER BLUE PULSE
# ============================================================

def update_rgb():
t = time.monotonic()

pulse = int(
20 + (math.sin(t * 4) + 1) * 25
)

for i in range(LED_COUNT):
variation = (i * 3) % 12

pixels[i] = (
0,
min(80, pulse // 3 + variation),
min(120, pulse + variation),
)

pixels.show()


# ============================================================
# OLED GLITCH DISPLAY
# ============================================================

glitch_text = [
"GLITCHPAD",
"GL1TCHPAD",
"GL!TCHPAD",
"GLITCHP4D",
]

frame = 0
last_oled_update = 0


def update_oled():
global frame
global last_oled_update

now = time.monotonic()

if now - last_oled_update < 0.18:
return

last_oled_update = now

oled.fill(0)

# Title
oled.text(
glitch_text[frame],
10,
0,
1,
)

# Status
oled.text(
"SYSTEM ONLINE",
5,
12,
1,
)

# Animated glitch bar
bar_length = (frame * 18) % 120

oled.fill_rect(
4,
23,
bar_length,
2,
1,
)

oled.text(
"READY",
48,
26,
1,
)

oled.show()

frame = (frame + 1) % len(glitch_text)


# ============================================================
# STARTUP
# ============================================================

oled.fill(0)
oled.text("GLITCHPAD", 25, 5, 1)
oled.text("BOOTING...", 25, 20, 1)
oled.show()

pixels.fill((0, 10, 30))
pixels.show()

time.sleep(1)

oled.fill(0)
oled.show()


# ============================================================
# KMK START
# ============================================================

if __name__ == "__main__":
keyboard.go()
