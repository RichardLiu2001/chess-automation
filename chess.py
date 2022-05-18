from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

driver = webdriver.Firefox()
#vegetable = driver.find_element(By.CLASS_NAME, "tomatoes")
url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
chess_url = "https://www.chess.com/play/online"
driver.get(chess_url)


change_time_button = driver.find_element(By.CLASS_NAME, "icon-font-chess.chevron-bottom.time-selector-chevron")
change_time_button.click()

bullet_button = driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-basic.ui_v5-button-small.ui_v5-button-full.time-selector-category-btn")
bullet_button.click()

play_button = driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")
play_button.click()

loading = True

while loading:
    try:
        guest_button = driver.find_element(By.ID, "guest-button")
        guest_button.click()
        loading = False
    except:
        continue

found_game = False

while not found_game:
    try:
        game_start = driver.find_element(By.CLASS_NAME, "draw-button-label")
        print(str(game_start))
        found_game = True
    except:
        time.sleep(2)
        print("not started")
        #print("No game found")


color = "black"

found_color = False

while not found_color:

    try:
        driver.find_element(By.CLASS_NAME, "clock-component clock-white clock-top clock-live clock-player-turn player-clock")
        found_color = True
    except:

        try:
            driver.find_element(By.CLASS_NAME, "clock-component.clock-black.clock-top.clock-live.player-clock")
            found_color = True
            color = "white"
        except:
            continue


#color = driver.find_element(By.CLASS_NAME, "clock-component.clock-white.clock-top.clock-live.clock-player-turn.player-clock")
print(str(color))