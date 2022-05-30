# todo: new games, rematch, autoqueen/promotions, set level

from multiprocessing.connection import wait
from unittest.mock import NonCallableMagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import threading

from Engine import Engine
from mouse import Clicker

driver = webdriver.Firefox()
chess_url = "https://www.chess.com"
driver.get(chess_url)


def hit_play():
    play_online_button = driver.find_element(By.CLASS_NAME, "index-guest-button.ui_v5-button-component.ui_v5-button-large.ui_v5-button-primary.ui_v5-button-full")
    play_online_button.click()

def play_as_guest():
    guest_button = driver.find_element(By.ID, "guest-button")
    guest_button.click() 

def change_to_bullet():
    change_time_button = driver.find_element(By.CLASS_NAME, "icon-font-chess.chevron-bottom.time-selector-chevron")
    change_time_button.click()
    bullet_button = driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-basic.ui_v5-button-small.ui_v5-button-full.time-selector-category-btn")
    bullet_button.click()

def set_level(level='Advanced'):
    level_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Advanced']")))
    level_button.click()
    level_button.click()
    print("here")

def find_match():
    play_button = driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")
    play_button.click()

def wait_game_start():
    # wait for draw button to appear
    WebDriverWait(driver, float('inf')).until(EC.presence_of_element_located((By.CLASS_NAME, "draw-button-label")))

def get_color():
    color = "black"
    opponent_color = 'white'

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
                opponent_color = 'black'
            except:
                continue
    return color, opponent_color

def wait_move(color, move_count):
    # return text of opponent move
    while True:
        try:
            return driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']')
        except:
            continue


def get_move(player_color, move_count):
    piece = None
    try:
        move_element = driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']').text
        try:
            piece_element = move_element.find_element(by=By.XPATH, value=".//*")
            piece = piece_element.get_attribute("data-figurine")
        except:
            piece = ""
        if piece == None:
            piece = ""
        return piece + move_element.text
        #return driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']').text
    except:
        move_element = wait_move(player_color, move_count)
        piece = None
        try:
            piece_element = move_element.find_element(by=By.XPATH, value=".//*")
            piece = piece_element.get_attribute("data-figurine")
        except:
            piece = ""
        if piece == None:
            piece = ""
        return piece + move_element.text

hit_play()
set_level()
play_as_guest()
change_to_bullet()



find_match()

# wait for draw button (match found)
wait_game_start()
color, opponent_color = get_color()
print("you are " + color)
engine = Engine()
clicker = Clicker(driver, color)
clicker.initialize_sizes()

# big loop to play multiple games
def play():

    wait_game_start()
    color, opponent_color = get_color()
    clicker.set_color(color)
    engine.reset()
    play_game(engine, color)

    # look for rematch for 8 seconds
    # hit new match
    #

# 1. 

def play_game(engine, color):

    move_count = 1
    opponent_color = 'white'

    if color == 'black':
        opponent_move = get_move('white', move_count)
        print("white move: " + opponent_move)
        engine.process_move(opponent_move)
        move_count += 1

    else:
        opponent_color = 'black'

    # new match button = ui_v5-button-component ui_v5-button-basic

    #while (no new match button):
    while True:
    # make and register move
        p1 = 'white'
        p2 = 'black'

        if move_count % 3 == 0:
            clicker.emoji()

        if move_count % 2 == 0:
            # this is black's move
            p1 = p2
            p2 = 'white'

        if p1 == color:
            uci, san = engine.get_engine_move()
            clicker.make_move(uci, san)

        p1_move = get_move(p1, move_count)
        print(p1 + " move: " + p1_move)
        engine.process_move(p1_move)
        move_count += 1

        if p2 == color:
            uci, san = engine.get_engine_move()
            print("suggested move: " + san)
            clicker.make_move(uci, san)

        p2_move = get_move(p2, move_count)
        print(p2 + " move: " + p2_move)
        engine.process_move(p2_move)
        move_count += 1

move_count = 1

opponent_color = 'white'

if color == 'black':
    opponent_move = get_move('white', move_count)
    print("white move: " + opponent_move)
    engine.process_move(opponent_move)
    move_count += 1

else:
    opponent_color = 'black'

while True:
    # make and register move
    p1 = 'white'
    p2 = 'black'

    if move_count % 3 == 0:
        clicker.emoji()

    if move_count % 2 == 0:
        # this is black's move
        p1 = p2
        p2 = 'white'

    if p1 == color:
        uci, san = engine.get_engine_move()
        clicker.make_move(uci, san)

    p1_move = get_move(p1, move_count)
    print(p1 + " move: " + p1_move)
    engine.process_move(p1_move)
    move_count += 1

    if p2 == color:
        uci, san = engine.get_engine_move()
        print("suggested move: " + san)
        clicker.make_move(uci, san)

    p2_move = get_move(p2, move_count)
    print(p2 + " move: " + p2_move)
    engine.process_move(p2_move)
    move_count += 1


    # poll new game:
    # poll rematch
    #rematch: ui_v5-button-icon icon-font-chess checkmark


