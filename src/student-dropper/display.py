import board
import busio
import adafruit_ssd1305
from PIL import Image, ImageDraw, ImageFont
import time

i2c = busio.I2C(board.SCL, board.SDA)

display = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c)

# OLED display stuff


def draw(mylist):
	index = 0
	image = Image.new('1', (128, 32)) 
	draw = ImageDraw.Draw(image)
	for item in mylist:
		draw.text((0, index), item, fill="white")
		index += 10
	
	display.image(image)
	display.show()
