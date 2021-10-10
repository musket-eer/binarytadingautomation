import pyautogui as auto
from PIL import ImageGrab,ImageOps
import pytesseract as tess
import cv2
import time
import datetime
import numpy as np

# this should automate trading in olymp by manipulating gui
def check_balance():
    """
    captures the written balance on olymp trade platform and saves it as an integer
    returns the balance as an int
    :return (float): returns the outstanding account balance
    """
    tess.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
    cap = ImageGrab.grab(bbox=(2162, 220, 2362, 314))
    cap = ImageOps.invert(cap.convert('RGB'))

    tesstsr = tess.image_to_string(cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2BGRA), lang='eng')
    tesstsr = [x for x in tesstsr if x.isdigit() or x == "."]
    tesstsr = "".join(tesstsr)
    
    return float(tesstsr)

def stop_loss(initial_balance):
    """
    sets the amount below which the trading should stop
    :param initial_balance(int): the starting account balance
    :return (int): returns 0.7 * the amount
    """
    return float(0.7 * initial_balance)

def take_profit(initial_balance):
    """
    sets the amount above which the trading should stop
    :param initial_balance(int): the starting account balance
    :return (int): returns 1.2 * the amount
    """
    return float(1.2 * initial_balance)


def stake_amount(amount):
    """
    sets the stake in the trading platform
    :param amount (int): the amount to be staked
    """

    auto.click(1348, 264) # text area for entering stake

    # delete characters 5 times to ensure that no char is in the stake area before typing anything
    for i in range(10):
        auto.press('backspace') 
    
    auto.typewrite(str(amount)) # enters the stake in the stake area

def execute_trade_up():
    """
    executes an up-trade
    """
    auto.click(1336, 456)
    print(datetime.datetime.now()) # prints the time for the trade

def execute_trade_down():
    """
    executes a dowm-trade
    """
    auto.click(1339, 545)
    print(datetime.datetime.now()) # prints the time for the trade

def reset_stake():
    """
    sets the stake in the trading platform
    :param amount (int): the amount to be staked
    """

    auto.click(1348, 264) # text area for entering stake

    # delete characters 5 times to ensure that no char is in the stake area before typing anything
    for i in range(5):
        auto.press('backspace') 
    
    auto.typewrite(str(0.01 * check_balance())) # enters the stake in the stake area


 
def on_profit(former_balance, current_balance):
    """
    checks whether a profit or loss was made after a single trade
    :param former_balance (float): balance before the trade
    :param current_balance (float): balance after the trade
    :return (bool): shows whether we are on profit (True) or not (False)
    """
    return current_balance >= former_balance


def main():
    # to give time to switch to olymp trade
    time.sleep(7)

    # sets the initial balance
    initial_balance = check_balance()

    # sets the stop loss
    loss_stop_reached = stop_loss(initial_balance) < 0.7 * initial_balance


    profit_take_reached = take_profit(initial_balance) > 1.2 * initial_balance
    stop_trade = loss_stop_reached or profit_take_reached
    stake = stake_amount(str(0.01 * initial_balance))
    trades = 0
    double_stake = 1

    while trades <= 80 or stop_trade:
        stake = stake_amount(str(0.01 * initial_balance * double_stake))
        execute_trade_up()
        trades += 1
        time.sleep(62)
        
        new_balance =  check_balance()
        if on_profit(initial_balance, new_balance):
            while on_profit(initial_balance, new_balance):
                stake = reset_stake()
                execute_trade_up()
                trades += 1
                time.sleep(62)
                initial_balance = new_balance

        else:
            double_stake *= 2
            stake = stake_amount(str(0.01 * initial_balance * double_stake))
            execute_trade_down()
            trades += 1
            time.sleep(62)
            new_balance = check_balance()
            while on_profit(initial_balance, new_balance):
                stake = reset_stake()
                execute_trade_down()
                trades += 1
                time.sleep(62)

        double_stake *= 2

        
        initial_balance = new_balance





if __name__ == "__main__":
    main()






