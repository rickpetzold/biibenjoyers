import numpy as np
import cv2
from PIL import Image
import pytesseract


def remove_noise(image):
    return cv2.medianBlur(image,5)

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 3)


def get_captcha():
    image = cv2.imread(r"temp/screen.png")
    crop = image[220:310, 300:470]
    cv2.imwrite(r"temp/crop.png", crop)
    image = cv2.imread("temp/crop.png")

    noise = remove_noise(image)
    grey = get_grayscale(noise)

    cv2.imwrite(r"temp/noise.png", grey)
    cap = pytesseract.image_to_string(grey).strip()
    
    return cap





    