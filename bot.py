"""
Snapchat web snapscore bot.

:author: Max Milazzo
"""


import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from time import time, sleep
from random import random
# manages imports


MY_USERNAME = "EXAMPLE@gmail.com"
MY_PASSWORD = "PASSWORD123"
# username and password

SLEEP_TIME = 1
# sleep time between actions (multiplied by random number from 0-1 PLUS MIN_MULT)

LOGIN_SLEEP = 1
# sleep time between login actions

SELECT_SLEEP = 0.01
# sleep time for chat selection (multiplied by random numbr from 0-1 PLUS MIN_MULT)

MIN_MULT = 0.05
# minimum value to add to random multiplier for sleeps

MIN_ADD = 0
# minimum value to add to random sleep times

CHAT_SELECTIONS = 100
# maximum value of chat selection (will select chats from index 1 to CHAT_SELECTIONS value)
# snaps will be sent to the FIRST "n" groups/people based on Snapchat's default (based on previoud send activity)
# if CHAT_SELECTIONS = N, then N snaps will be sent per "batch"

ERR_SEND_RATE_MULT = 20
# estimation of number of additional "lost" snaps per failed batch
# a previously failed batch can interfere with the next batch, and even if successful it can cause some sends to fail

FIRST_SEND_SLEEP = 30
# waits extra time after the first snap send

USERNAME = '//*[@id="username"]'
PASSWORD = '//*[@id="password"]'
LOGIN = '//*[@id="loginTrigger"]'
# login XPATH data

CAMERA = '//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]'
SEND_1 = '//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/button[2]'
SEND_2 = '//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/form/div[4]/button'
RESTART_CAM = '//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/button'
TEST_OPEN = '//*[@id="root"]/div[1]/div[1]/div[1]/div[3]/button'
# element XPATH data
# selection XPATH data stored and handled in "send_pic" function

batch_num = 1
# batch number count

err_count = 0
# error counter

successful_batches = 0
# successful batch count

failed_batches = 0
# failed batch count

send_count = 0
# snap send counter


def init():
    """
    Creates driver and opens site.
    
    :return: driver
    :rtype: webdriver
    """

    driver = uc.Chrome(use_subprocess=True)
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
    
    global batch_num
    global err_count
    global send_count
    global successful_batches
    global failed_batches
    # global variables used
    
    selected_count = 0
    batch_err = 0
    batch_start = time()
    # temporary local variables used
    
    sleep(SLEEP_TIME * (random() + MIN_MULT) + 3)
    # sleep(SLEEP_TIME * (random() + MIN_MULT) + MIN_ADD)
    # [ custom sleep time used for better results ]
    # waits before after next iteration called in main
       
    try:
        camera_elem = driver.find_element(By.XPATH, CAMERA)
        camera_elem.click()
        print("[ camera click SUCCESS ]")
        # clicks camera
        
    except Exception as e:
        err_count += 1
        batch_err += 1
        
        print("[ camera click FAILURE ]")
        print(f"Error #{err_count}:\n----------")
        print(e)
        
    sleep(SLEEP_TIME * (random() + MIN_MULT) + MIN_ADD)
    # waits after clicking camera
    
    try:
        send_1_elem = driver.find_element(By.XPATH, SEND_1)
        send_1_elem.click()
        print("[ send (1/2) click SUCCESS ]")
        # clicks "send"
        
    except Exception as e:
        err_count += 1
        batch_err += 1
        
        print("[ send (1/2) click FAILURE ]")
        print(f"Error #{err_count}:\n----------")
        print(e)
        
    sleep(SLEEP_TIME * (random() + MIN_MULT) + 3)
    # sleep(SLEEP_TIME * (random() + MIN_MULT) + MIN_ADD)
    # [ custom sleep time used for better results ]
    # waits after "send" click
    
    try:
        for x in range(1, CHAT_SELECTIONS + 1):
            select_elem = driver.find_element(By.XPATH, f'//*[@id="root"]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/form/div[3]/div/div[1]/div[{x}]/div[3]')
            # select button string
            # changes based on selection, so not included as global variable
            
            select_elem.click()

            selected_count += 1
            print(f"[ select ({x}/{CHAT_SELECTIONS}) click SUCCESS ]")
            
            sleep(SELECT_SLEEP * (random() + MIN_MULT) + MIN_ADD)
            # clicks select and waits
            
    except Exception as e:
        err_count += 1
        batch_err += 1
        
        print(f"[ select click FAILURE ]")
        print(f"Error #{err_count}:\n----------")
        print(e)
        
    sleep(SLEEP_TIME * (random() + MIN_MULT) + MIN_ADD)
    # waits additional time after selection
    
    try:
        send_2_elem = driver.find_element(By.XPATH, SEND_2)
        send_2_elem.click()
        send_count += selected_count
        print("[ send (2/2) click SUCCESS ]")
        # clicks final send
        
    except Exception as e:
        err_count += 1
        batch_err += 1
        
        print("[ send (2/2) click FAILURE ]")
        print(f"Error #{err_count}:\n----------")
        print(e)
    
    if batch_err == 0:  # updates batch success/failure data
        successful_batches += 1
    else:
        failed_batches += 1
        
    cur_time = time()
    
    print("\n" + "=" * 80)
    print(f"Batch #{batch_num}:")
    print("=" * 80)
    print(f"BATCH COUNT: << {selected_count} snaps selected in batch >>")
    print(f"BASE TOTAL COUNT: << {send_count} snaps sent in total >>")
    print(f"EST. ACTUAL COUNT: << {round(send_count - failed_batches * ERR_SEND_RATE_MULT)} snaps sent in total >>")
    print(f"\nBATCH TIME: << {round(cur_time - batch_start, 3)} seconds elapsed in batch >>")
    print(f"TOTAL TIME: << {round(cur_time - START_TIME, 3)} seconds elapsed in total >>")
    print(f"\nBATCH ERRORS: << {batch_err} >>")
    print(f"TOTAL ERRORS: << {err_count} >>")
    print(f"\nCLEAN BATCHES: << {successful_batches} >>")
    print(f"ERRORED BATCHES: << {failed_batches} >>")
    print(f"\nBATCH RATE: << {round(selected_count / (cur_time - batch_start), 3)} snaps/second >>")
    print(f"CUM. BASE RATE: << {round(send_count / (cur_time - START_TIME), 3)} snaps/second >>")
    print(f"EST. CUM. ACTUAL RATE: << {round((send_count - failed_batches * ERR_SEND_RATE_MULT) / (cur_time - START_TIME), 3)} snaps/second >>")
    print("=" * 80 + "\n")
    # displays data
    
    if batch_num == 1:  # extra sleep after first send
        sleep(FIRST_SEND_SLEEP)
    
    try:
        driver.find_element(By.XPATH, TEST_OPEN)
        # this data should always be present on page
        
    except:
        driver.refresh()
        sleep(5)
        # refresh if page error
        # some sleep value (can change based on user preference)
        
    try:
        start_cam = driver.find_element(By.XPATH, RESTART_CAM)
        start_cam.click()
        # attempts to click "cam restart" button if needed
        
    except:
        pass
            
    batch_num += 1


def main():
    """
    Program entry point.
    """
    
    global START_TIME
    
    driver = init()
    login(driver)
    # gets driver and logs in
    
    input("Complete camera setup and press enter to start...")
    print("<< PROGRAM RUNNING >>")
    
    START_TIME = time()
    
    while (True):  # loops to send snaps indefinitely
        send_pic(driver)


if __name__ == "__main__":
    main()