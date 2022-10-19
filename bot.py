"""
Snapchat web snapscore bot.

:author: Max Milazzo
"""


import undetected_chromedriver as uc
# undetectable chromedriver import in run folder

from selenium.webdriver.common.by import By
from time import sleep
from random import random
# manages additional imports


MY_USERNAME = "USERNAME/EMAIL"
MY_PASSWORD = "PASSWORD"
# username and password

SLEEP_TIME = 1
# sleep time between actions (multiplied by random number from 0-1 PLUS MIN_MULT)

LOGIN_SLEEP = 1
# sleep time between login actions

SELECT_SLEEP = 0.3
# sleep time for chat selection (multiplied by random numbr from 0-1 PLUS MIN_MULT)

MIN_MULT = 0.05
# minimum value to add to random multiplier for sleeps

CHAT_SELECTIONS = 100
# maximum value of chat selection (will select chats from index 1 to CHAT_SELECTIONS value)

USERNAME = '//*[@id="username"]'
PASSWORD = '//*[@id="password"]'
LOGIN = '//*[@id="loginTrigger"]'
# login XPATH data

CAMERA = '//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]'
SEND_1 = '//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/button[2]'
SEND_2 = '//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/form/div[4]/button'
# element XPATH data
# selection XPATH data stored and handled in "send_pic" function


def init():
    """
    Creates driver and opens site.
    
    :return: driver
    :rtype: webdriver
    """

    driver = uc.Chrome()
    driver.get("http://web.snapchat.com/")
    
    input("Wait for site to load (login button MUST be yellow), then press enter to continue...")
    
    return driver


def login(driver):
    """
    Logs into site.
    
    :param driver: current webdriver in use
    :type driver: webdriver
    """
    
    username_elem = driver.find_element(By.XPATH, USERNAME)
    username_elem.send_keys(MY_USERNAME)
    # enters username
    
    sleep(LOGIN_SLEEP)
    
    password_elem = driver.find_element(By.XPATH, PASSWORD)
    password_elem.send_keys(MY_PASSWORD)
    # enters password
    
    sleep(LOGIN_SLEEP)
    
    login_elem = driver.find_element(By.XPATH, LOGIN)
    login_elem.click()
    # clicks login button


def send_pic(driver):
    """
    Sends a single snap to chats.
    
    :param driver: current webdriver in use
    :type driver: webdriver
    """
       
    try:
        camera_elem = driver.find_element(By.XPATH, CAMERA)
        camera_elem.click()
    except Exception as e:
        print(e)
        
    sleep(SLEEP_TIME * (random() + MIN_MULT))
    # clicks camera and waits
    
    try:
        send_1_elem = driver.find_element(By.XPATH, SEND_1)
        send_1_elem.click()
    except Exception as e:
        print(e)
        
    sleep(SLEEP_TIME * (random() + MIN_MULT))
    # clicks "send" and waits
    
    try:
        for x in range(1, CHAT_SELECTIONS + 1):
            select_elem = driver.find_element(By.XPATH, f'//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/form/div[3]/div/div[1]/div[{x}]/div[3]')
            # select button string
            # changes based on selection, so not included as global variable
            
            select_elem.click()
            sleep(SELECT_SLEEP * (random() + MIN_MULT))
            # clicks select and waits
            
    except Exception as e:
        print(e)
        
    sleep(SLEEP_TIME * (random() + MIN_MULT))
    # waits additional time after selection
    
    try:
        send_2_elem = driver.find_element(By.XPATH, SEND_2)
        send_2_elem.click()
    except Exception as e:
        print(e)
        
    sleep(SLEEP_TIME * (random() + MIN_MULT))
    # clicks final send then waits before next iteration called in main


def main():
    """
    Program entry point.
    """
    
    driver = init()
    login(driver)
    # gets driver and logs in
    
    input("Complete camera setup and press enter to start...")
    print("<< PROGRAM RUNNING >>")
    
    while (True):  # loops to send snaps indefinitely
        send_pic(driver)


if __name__ == "__main__":
    main()