import numpy as np
import cv2
from PIL import Image
import pytesseract
from os import path


def remove_noise(image):
    return cv2.medianBlur(image,5)

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 3)


def get_captcha():
    # Absolute paths
    file_path = path.abspath(__file__)
    dir_path = path.dirname(file_path)

    img_path = path.join(dir_path, "temp/screen.png")
    crop_path = path.join(dir_path, "temp/crop.png")
    noise_path = path.join(dir_path, "temp/noise.png")

    # Get image from login captcha
    image = cv2.imread(img_path)

    # Crop, reduce noise and apply grey
    crop = image[220:310, 290:460]
    cv2.imwrite(crop_path, crop)
    image = cv2.imread(crop_path)

    noise = remove_noise(image)
    grey = get_grayscale(noise)
    cv2.imwrite(noise_path, grey)

    # Get captcha text 
    cap = pytesseract.image_to_string(grey).strip()
    
    return cap





    