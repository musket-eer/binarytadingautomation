from sys import _current_frames
import pyautogui as auto
from PIL import ImageGrab,ImageOps
import pytesseract as tess
import cv2
import time
import datetime
import numpy as np
from math import pow

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

    # extracts, from the image, only characters of numerical significance(ignoring currency symbols etc)
    tesstsr = [x for x in tesstsr if x.isdigit() or x == "."]
    tesstsr = "".join(tesstsr)
    
    return float(tesstsr)

def stop_loss(initial_balance, current_balance):
    """
    sets the amount below which the trading should stop
    :param initial_balance(int): the starting account balance
    :return (int): returns 0.85 * the amount
    """
    return (float(0.7 * initial_balance)) >= float(current_balance)

def take_profit(initial_balance, current_balance):
    """
    sets the amount above which the trading should stop
    :param initial_balance(int): the starting account balance
    :return (int): returns 1.4 * the amount
    """
    return (float(1.2 * initial_balance)) <= float(current_balance)


def stake_amount(amount):
    """
    sets the stake in the trading platform
    :param amount (int): the amount to be staked
    """

    auto.click(1348, 264) # text area for entering stake

    # delete characters 5 times to ensure that no character is in the stake area before typing anything
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

 
def on_profit(former_balance, current_balance):
    """
    checks whether a profit or loss was made after a single trade
    :param former_balance (float): balance before the trade
    :param current_balance (float): balance after the trade
    :return (bool): shows whether we are on profit (True) or not (False)
    """
    return current_balance >= former_balance


def main():
    # time allowance for switching to online trading platform 
    time.sleep(5)

    # checks the initial balance
    initial_bal = check_balance()
    stake_dec = 0.0028899
    timeout = 62

    # sets both bal1 and bal2 to the initial balance
    bal1 = initial_bal
    bal2 = initial_bal

    # set a balance below which trading stops
    

    # sets a bool for exiting trade
    
    # counter to keep track of the number of trades
    trades = 0

    # variable for loss recovery
    compensator = 0
    trade_exit =  stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2)

    # daily target for the number of trades to be executed
    target = 1000
    comp = 2.25
    log_file = open("demo_logs.txt", "a")

    log_file.write(f'\n\n')
    log_file.write(f'{datetime.datetime.now()}\n\n')

    # loop for continuously executing trades until conditions for exit are met
    while trades <= target and not trade_exit:
       
        # sets the compensator to zero in case of a successful trade
        if on_profit(bal1, bal2):
            compensator = 0

        # sets the stake for the first trade
        stake_amount(stake_dec * initial_bal * pow(comp, compensator)) 

        # picks an up trade
        execute_trade_up()
        trades += 1
        time.sleep(timeout)

        bal2 = check_balance()
        trade_exit = stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2)
        if bal2 > stop_loss(initial_bal, bal2):
                trade_exit = False
        print(trade_exit)
        
        
        


        log_file.write(f'{trades}; {bal1}, {bal2}, {on_profit(bal1, bal2)}\n')
       



        # keeps on executing the same trade until one trade results in a loss
        while on_profit(bal1, bal2):
            compensator = 0
            stake_amount(stake_dec * bal2)
            execute_trade_up()
            trades += 1
            time.sleep(timeout)
            bal1 = bal2
            bal2 = check_balance()
            trade_exit = stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2)
            if bal2 > stop_loss(initial_bal, bal2):
                trade_exit = False
            print(trade_exit)
            

            log_file.write(f'{trades}; {bal1}, {bal2}, {on_profit(bal1, bal2)}\n')
            


        compensator += 1

        # executes a down trade if any up trade results in a loss
        stake_amount(stake_dec * initial_bal * pow(comp, compensator))
        execute_trade_down()
        trades += 1
        time.sleep(timeout)
        bal1 = bal2
        bal2 = check_balance()
        trade_exit = stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2)
        if bal2 > stop_loss(initial_bal, bal2):
                trade_exit = False
        print(trade_exit)
        
        

        log_file.write(f'{trades}; {bal1}, {bal2}, {on_profit(bal1, bal2)}\n')

        # keeps on executing down trades after every profitable down trade
        while on_profit(bal1, bal2):
            compensator = 0
            stake_amount(stake_dec * bal2)
            execute_trade_down()
            trades += 1
            time.sleep(timeout)
            bal1 = bal2
            bal2 = check_balance()
            trade_exit = stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2)
            if bal2 > stop_loss(initial_bal, bal2):
                trade_exit = False
            print(trade_exit)
            
            
            log_file.write(f'{trades}; {bal1}, {bal2}, {on_profit(bal1, bal2)}\n')
           
        
        
        compensator += 1
        trades  += 1


    log_file.write(f'{trades}\n')
    # prints the days profit or loss(when there is a negative value)
    log_file.write(f'{check_balance() - initial_bal}\n')
    log_file.close()




if __name__ == "__main__":
    main()






