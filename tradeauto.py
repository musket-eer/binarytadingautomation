import pyautogui as auto
from PIL import ImageGrab,ImageOps
import pytesseract as tess
import cv2
import time
from datetime import datetime, date
import calendar
import numpy as np
from math import pow, sqrt

def check_balance():
    """
    captures the written balance on olymp trade platform and saves it as an integer
    returns the balance as an int
    :return (float): returns the outstanding account balance
    """
    tess.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
    cap = ImageGrab.grab(bbox=(2162, 220, 2362, 314)) # captures part of the screen on the trading platform that shows the account balance
    cap = ImageOps.invert(cap.convert('RGB')) # converts the captured image to rgb, then inverts the colors for enhanced character distinction

    tesstsr = tess.image_to_string(cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2BGRA), lang='eng')

    # extracts, from the image, only characters of numerical significance(ignoring currency symbols etc)
    tesstsr = [x for x in tesstsr if x.isdigit() or x == "."]
    tesstsr = "".join(tesstsr)
    
    print(float(tesstsr))
    return float(tesstsr)

def stop_loss(initial_balance, current_balance):
    """
    sets the amount below which the trading should stop
    :param initial_balance(int): the starting account balance
    :return (bool): returns True if the current balance is less than or equal to the set stop loss, else returns False
    """
    return (int(0.3 * initial_balance)) >= int(current_balance)

def take_profit(initial_balance, current_balance):
    """
    sets the amount above which the trading should stop
    :param initial_balance(int): the starting account balance
    :return (bool): returns True if the current balance is greater than or equal to the set take profit percentage, else returns False
    """
    return (int(1.006 * initial_balance)) <= int(current_balance)


def stake_amount(amount):
    """
    sets the stake in the trading platform
    :param amount (int): the amount to be staked
    """
    # clicks the trading platform's set stake area
    auto.click(1348, 264) # text area for entering stake

    # delete characters 5 times to ensure that no character is in the stake area before typing anything
    for i in range(10):
        auto.press('backspace') 
    
    auto.typewrite(str(amount)) # enters the stake in the stake area

def execute_trade_up():
    """
    executes an up-trade
    """
    # clicks the trading platform's execute trade up button
    auto.click(1336, 456)
    print(datetime.now()) # prints the time for the trade

def execute_trade_down():
    """
    executes a down-trade
    """
    # clicks the trading platform's execute trade down button
    auto.click(1319, 535)
    print(datetime.now()) # prints the time for the trade

 
def on_profit(former_balance, current_balance):
    """
    checks whether a profit or loss was made after a single trade
    :param former_balance (float): balance before the trade
    :param current_balance (float): balance after the trade
    :return (bool): returns True if current balance is greater than or equal to former balance, else returns False
    """
    return current_balance >= former_balance
    
def record_trade(trades, start, stop, counter):

    filename = "demo_logs_final.csv"
    log_file = open(filename, "a")

    profit = (stop - start) / start * 100
    log_file.write(f'{trades:}, ({start},{stop},({counter}, {profit}\n')
    log_file.close()


def main():
    # time allowance for switching to online trading platform 
    time.sleep(5)

    # checks the initial balance
    initial_bal = check_balance()
    stake_dec = 1.01 / initial_bal
    main_timeout= 61.5
    timeout1 = 1.5 # for checking a bal at the middle of a trade


    # sets bal1, bal2 and bal3 to the initial balance
    bal1 = initial_bal # bal before a trade is executed
    bal2 = initial_bal # bal after a trade is executed but before it closes
    bal3 = initial_bal # bal at the close of a trade

    # a bool to keep track of whether stop loss or take profit as been attained
    trade_exit =  stop_loss(initial_bal, bal3) or take_profit(initial_bal, bal3)

    # daily target for the number of trades to be executed
    target = 1000
    comp = 1.0 # a factor for multiplying the stake amount to recover losses
    filename = "demo_logs.csv"
    log_file = open(filename, "a")

    # variables for adjusting the stake amount incase of a loss
    compensator = 0 # for powering comp after each lost trade 
    trades = 0 # tracker for counting the number of trades opened
    proff = 0.8
    # loop for continuously executing trades until conditions for exit are met
    while trades <= target and not trade_exit:

        # sets the stake for the first trade
        stake_amount(stake_dec * initial_bal * pow(comp, compensator)) 

        # picks an up trade
        execute_trade_up()
        time.sleep(timeout1)
        bal2 = check_balance() # records the balance shortly after the trade has been executed. if this bal is same as one before the trade, then the network lagged
        # exiting the main loop incase of a network lag
        if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal3):
                break

        if bal2 == bal1:
            print("network lag")
            break

        trades += 1
        time.sleep(main_timeout)

        bal3 = check_balance()
        
        print(trade_exit, bal3 - bal1)

        log_file.write(f'{trades}, {bal3}\n')
       
        # keeps on executing the same trade until one trade results in a loss
        while on_profit(bal1, bal3):
            compensator = 0
            comp = 1.0
            proff = 0.8
            stake_amount(stake_dec * initial_bal)
            execute_trade_up()
            time.sleep(timeout1)

            # stops executing trades if the network lag occurs within the main loop
            if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2):
                break

            if bal2 == bal1:
                compensator = -1
                print("network lag")
                break

            trades += 1
            time.sleep(main_timeout)
            bal1 = bal3
            bal3 = check_balance()
            trade_exit = stop_loss(initial_bal, bal3) or take_profit(initial_bal, bal3)
            print(trade_exit, bal3 - bal1)
            

            log_file.write(f'{trades}, {bal3}\n')
            
        proff *= 1.05
        compensator += 0.5 * proff
        comp += 0.3 * sqrt(proff)

        # executes a down trade if any up trade results in a loss
        stake_amount(stake_dec * initial_bal * pow(comp, compensator))
        execute_trade_down()
        time.sleep(timeout1)
        bal2 = check_balance()

        # exiting the main loop incase of a network lag
        if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2):
                break

        if bal2 == bal1:
            print("network lag")
            time.sleep(main_timeout)
            break

        trades += 1
        time.sleep(main_timeout)
        bal1 = bal3
        bal3 = check_balance()
        trade_exit = stop_loss(initial_bal, bal3) or take_profit(initial_bal, bal3)
        print(trade_exit, bal3 - bal1)
        
        log_file.write(f'{trades}, {bal3}\n')

        # keeps on executing down trades after every profitable down trade
        while on_profit(bal1, bal3):
            compensator = 0
            comp = 1.0
            proff = 0.8
            stake_amount(stake_dec * initial_bal)
            execute_trade_down()
            time.sleep(timeout1)

            if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal3):
                break

            # stops executing trades if the network lag occurs within the main loop
            if bal2 == bal1:
                compensator = -1
                print("network lag")
                time.sleep(main_timeout)
                break

            trades += 1
            time.sleep(main_timeout)
            bal1 = bal3
            bal3 = check_balance()
            if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2):
                break

            print(trade_exit, bal3 - bal1)
            
            log_file.write(f'{trades}, {bal3}\n')
            
        # sets the compensator to zero in case of a successful trade. This resets the stake amount
        if on_profit(bal1, bal3):
            compensator = 0
            comp = 1.0
            proff = 0.8
        else:
            proff *= 1.05
            compensator += 0.5 * proff
            comp += 0.3 * sqrt(proff)


        trades  += 1

    log_file.write(f'{trades}\n')
    # prints the days profit or loss(when there is a negative value)
    log_file.write(f'{check_balance() - initial_bal}\n\n\n')
    log_file.close()


def main2():
    # check the balance
    time.sleep(5)
    initial_bal = check_balance()
    bal1 = initial_bal
    bal2 = initial_bal
    bal3 = initial_bal
   
    stake_dec = 1.01 / check_balance()
    main_timeout= 61.5
    timeout1 = 1.5 # for checking a bal at the middle of a trade

    # establish control variables, eg no of trades, trade exit, 

    trade_exit =  stop_loss(initial_bal, bal3) or take_profit(initial_bal, bal3)

    # daily target for the number of trades to be executed
    target = 1000
    comp = 1.4 # a factor for multiplying the stake amount to recover losses
    

    # variables for adjusting the stake amount
    compensator = 0 # for powering comp after each lost trade 
    trades = 0 # tracker for counting the number of trades opened
    proff = 1

    filename = "demo_logs2.csv"
    log_file = open(filename, "a")
    
    while trades < target and not trade_exit:
        if on_profit(bal1, bal3):
            comp = 1.4
            compensator = 0
            proff = 0
            stake_amount(stake_dec * initial_bal)
            execute_trade_up()
            
        else:
            proff *= 2
            comp += 0.2
            compensator += 0.5 + proff
            stake_amount(stake_dec * initial_bal * pow(comp, compensator))
            execute_trade_up()
            
        trades += 1
        time.sleep(timeout1)
        bal2 = check_balance()


        if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2):
            break

        if bal2 == bal1:
            print('network lag')
            break

        time.sleep(main_timeout)
        bal1 = bal3
        bal3 = check_balance()

        log_file.write(f'{trades}, {bal3}\n')

        if on_profit(bal1, bal3):
            proff = 0
            comp = 1.4
            compensator = 0
            stake_amount(stake_dec * initial_bal)
            execute_trade_down()
        else:
            proff *= 2
            comp += 0.2
            compensator += 0.5 + proff
            stake_amount(stake_dec * initial_bal * pow(comp, compensator))
            execute_trade_down()
            
        time.sleep(timeout1)
        bal2 = check_balance()

        if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal2):
            break

        if bal2 == bal1:
            print('network lag')
            break

        time.sleep(main_timeout)
        bal1 = bal3
        bal3 = check_balance()

        trades += 1

        log_file.write(f'{trades}, {bal3}\n')
        prof = bal3 - initial_bal
        perc = int(prof / initial_bal * 100)
        print(perc, bal3)

    log_file.write(f'{trades}, {bal3}\n')
    log_file.close()


def main3():
     # time lapse for switching windows
    time.sleep(5)

    # check the balance
    initial_bal = check_balance()
    bal1 = initial_bal
    bal2 = initial_bal
    bal3 = initial_bal
    x = 1.01
    y = 1
    z = 1
    stake_dec = x / check_balance()
    main_timeout = 60
    timeout1 = 3 # for checking a bal at the middle of a trade

    # daily target for the number of trades to be executed
    target = 1000
    trades = 0 # tracker for counting the number of trades opened
    stake = stake_dec * initial_bal

    # a tuple for all the stakes
    stakes = (1.01, 1.7, 3.8, 8.50, 22.00, 60.00, 140.00, 300.00, 700.00, 1460.00, 2900.00)
    stakes_counter = 0
    while trades < target:
        if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal3):
                break

        for i in range(3):
            stake_amount(stake)
            execute_trade_up()
            trades += 1
            time.sleep(timeout1)
            bal2 = check_balance()

            if bal1 == bal2:
                print("network lag")
                break
        
            time.sleep(main_timeout)
            bal1 = bal3
            bal3 =check_balance()

            if on_profit(bal1, bal3):
                stakes_counter = 0
                y = 1
                z = 1
               
            else:
                stakes_counter += 1
                y += 0.03
                z += 0.03
               
            x = stakes[stakes_counter] * y * z
            stake_dec = x / initial_bal
            stake = stake_dec * initial_bal

            if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal3):
                break

            record_trade(trades, bal1, bal3, stakes_counter + 1)

        if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal3):
                break

        if bal1 == bal2:
            print("network lag")
            break
            
        for i in range(3):
            stake_amount(stake)
            execute_trade_down()
            trades += 1
            time.sleep(timeout1)
            bal2 = check_balance()

            if bal1 == bal2:
                print("network lag")
                break

            time.sleep(main_timeout)
            bal1 = bal3
            bal3 =check_balance()

            if on_profit(bal1, bal3):
                stakes_counter = 0
                y = 1
                z = 1
                
            else:
                stakes_counter += 1
                y += 0.03
                z += 0.03
                
            x = stakes[stakes_counter] * y * z
            stake_dec = x / initial_bal
            stake = stake_dec * initial_bal

            if stop_loss(initial_bal, bal2) or take_profit(initial_bal, bal3):
                break
            
            record_trade(trades, bal1, bal3, stakes_counter + 1)

            if bal1 == bal2:
                print("network lag")
                break

            
   
if __name__ == "__main__":
    main3()





