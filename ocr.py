import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from sys import argv

image = Image.open(argv[1])

print pytesseract.image_to_string(image)

