# this file is for testing the functioning of different parts of the main file
# I have especially used it to test how 

from re import S
from numpy.lib.function_base import digitize
import pyautogui as auto
import time
import pytesseract as tess
from PIL import ImageGrab, ImageOps
import cv2
import numpy as np
import tradeauto
import datetime


time.sleep(5)
tess.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/5.2.0/bin/tesseract'
cap = ImageGrab.grab(bbox=(1100, 118, 1187, 137)) # captures part of the screen on the trading platform that shows the account balance
# cap = ImageOps.invert(cap.convert('RGB')) # converts the captured image to rgb, then inverts the colors for enhanced character distinction
cap.show()
tesstsr = tess.image_to_string(cv2.cvtColor(np.array(cap), cv2.THRESH_BINARY), lang='eng')


# extracts, from the image, only characters of numerical significance(ignoring currency symbols etc)
tesstsr = list([tesstsr][1:])
# tesstsr = "".join(tesstsr)
print(tesstsr)

# cap.show()

    

    
        


