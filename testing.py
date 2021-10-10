from numpy.lib.function_base import digitize
import pyautogui as auto
import time
import pytesseract as tess
from PIL import ImageGrab, ImageOps
import cv2
import numpy as np
import tradeauto


time.sleep(5)

intitial_bal = tradeauto.check_balance()
bal1 = float(tradeauto.check_balance())
bal2=float(tradeauto.check_balance())

trades = 0
compensator = 1
while trades <= 80:
    tradeauto.stake_amount(0.01 * bal1 * compensator)
    tradeauto.execute_trade_up()
    trades += 1
    time.sleep(61)
    bal2 = tradeauto.check_balance()
    while tradeauto.on_profit(bal1, bal2):
        tradeauto.reset_stake()
        tradeauto.execute_trade_up()
        trades += 1
        time.sleep(61)
        bal1 = bal2
        bal2 = tradeauto.check_balance()

    compensator *= 2
    tradeauto.stake_amount(0.01 * bal1 * compensator)
    tradeauto.execute_trade_down()
    trades += 1
    time.sleep(61)
    bal1 = bal2
    bal2 = tradeauto.check_balance()

    while tradeauto.on_profit(bal1, bal2):
        tradeauto.reset_stake()
        tradeauto.execute_trade_down()
        trades += 1
        time.sleep(62)
        bal1 = bal2
        bal2 = tradeauto.check_balance()

    trades  += 1

print(trades)
print(tradeauto.check_balance() - intitial_bal)


    
        


