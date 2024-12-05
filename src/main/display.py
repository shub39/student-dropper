import time

import board
import busio
import adafruit_ssd1305

from PIL import Image, ImageDraw, ImageFont
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c)


def draw(string_list, sleep_seconds = 0):
    index = 0
    image = Image.new('1', (128, 32))
    drawer = ImageDraw.Draw(image)
    for item in string_list:
        drawer.text((0, index), item.capitalize(), fill="white")
        index += 10

    display.image(image)
    display.show()
    time.sleep(sleep_seconds)