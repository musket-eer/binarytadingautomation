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

bal1 = intitial_bal
bal2 = 0
trades = 0
compensator = 0
while trades <= 80:
    if tradeauto.on_profit(bal1, bal2):
        compensator = 0

    tradeauto.stake_amount(0.01 * bal1 * 2 ** compensator)
    tradeauto.execute_trade_up()
    trades += 1
    time.sleep(62)
    bal2 = tradeauto.check_balance()
    print(trades, bal1, bal2, tradeauto.on_profit(bal1, bal2))

    while tradeauto.on_profit(bal1, bal2):
        compensator = 0
        tradeauto.stake_amount(0.01 * bal2)
        tradeauto.execute_trade_up()
        trades += 1
        time.sleep(62)
        bal1 = bal2
        bal2 = tradeauto.check_balance()
        print(trades, bal1, bal2, tradeauto.on_profit(bal1, bal2))


    compensator += 1

    tradeauto.stake_amount(0.01 * bal1 * 2 ** compensator)
    tradeauto.execute_trade_down()
    trades += 1
    time.sleep(62)
    bal1 = bal2
    bal2 = tradeauto.check_balance()
    print(trades, bal1, bal2, tradeauto.on_profit(bal1, bal2))

    while tradeauto.on_profit(bal1, bal2):
        compensator = 0
        tradeauto.stake_amount(0.01 * bal2)
        tradeauto.execute_trade_down()
        trades += 1
        time.sleep(62)
        bal1 = bal2
        bal2 = tradeauto.check_balance()
        print(trades, bal1, bal2, tradeauto.on_profit(bal1, bal2))
        
        
    compensator += 1
    trades  += 1


print(trades)
print(tradeauto.check_balance() - intitial_bal)


    
        


