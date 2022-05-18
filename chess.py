from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
chess_url = "https://www.chess.com/play/online"
driver.get(chess_url)


def change_to_bullet():
    change_time_button = driver.find_element(By.CLASS_NAME, "icon-font-chess.chevron-bottom.time-selector-chevron")
    change_time_button.click()
    bullet_button = driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-basic.ui_v5-button-small.ui_v5-button-full.time-selector-category-btn")
    bullet_button.click()

def find_match():

    # click play
    play_button = driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")
    play_button.click()

    # click play as guest
    guest_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "guest-button")))
    guest_button.click()

def wait_game_start():
    # wait for draw button to appear
    WebDriverWait(driver, float('inf')).until(EC.presence_of_element_located((By.CLASS_NAME, "draw-button-label")))

def get_color():
    color = "black"

    found_color = False
    while not found_color:
        try:
            driver.find_element(By.CLASS_NAME, "clock-component.clock-black.clock-bottom.clock-live.clock-running.player-clock.clock-player-turn")
            found_color = True
        except:
            try:
                driver.find_element(By.CLASS_NAME, "clock-component.clock-black.clock-top.clock-live.clock-running.player-clock")
                found_color = True
                color = "white"
            except:
                continue
    
    return color

def wait_opponent_move(my_color):
    # return text of opponent move
    element = WebDriverWait(driver, float('inf')).until(
        EC.presence_of_element_located((By.CLASS_NAME, my_color + ".node.selected"))
    )

    return element.text



change_to_bullet()
find_match()
wait_game_start()
color = get_color()


print("your color is :" + str(color))
black_move = None
white_move = None

if color == "white":
    time.sleep(3)


if color == 'black':
    opponent_move = wait_opponent_move(color)
    print(opponent_move)

move_count = 1
most_recent_move_element = driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']')
most_recent_move_text = most_recent_move_element.text

print("most recent move: " + most_recent_move_text)

move_count += 2
most_recent_move_element = driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']')
most_recent_move_text = most_recent_move_element.text

print("most recent move: " + most_recent_move_text)