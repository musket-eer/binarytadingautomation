# this file is for testing the functioning of different parts of the main file

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


init_bal = 200
bal = 900
bal2 = 200
exit_trade = not (tradeauto.stop_loss(init_bal, bal2) or tradeauto.take_profit(init_bal, bal2))
count = 0

while count <= 8 and exit_trade:
    bal2 -= 10
    print(bal2, count)
    count += 1
    print(datetime.datetime.now())

    

    
        


