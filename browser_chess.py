# todo: bug with aborted games (not hitting new game?)
# might be because weird exception with new game element is stale. idk
# sometimes doesnt accept rematch?

# ValueError: invalid san: 'h1=+Q'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import threading
from threading import Event
import time
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
    level_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='" + level + "']")))
    level_button.click()
    level_button.click()

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

def wait_move(move_count, in_game_condition):
    # return text of opponent move
    
    while in_game_condition.is_set():
        try:
            return driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']')
        except:
            continue
    
    # game ended before a move was made
    return None

def get_move(move_count, in_game_condition):
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
        move_element = wait_move(move_count, in_game_condition)

        # game ended before they made the move, return None
        if move_element is None:
            return None
        piece = None
        try:
            piece_element = move_element.find_element(by=By.XPATH, value=".//*")
            piece = piece_element.get_attribute("data-figurine")
        except:
            piece = ""
        if piece == None:
            piece = ""
        return piece + move_element.text

def check_website_in_game():
    try:
        # if there is the draw button, you are in a game
        driver.find_element(By.CLASS_NAME, "draw-button-label")
        return True
    except:
        return False

# runs every 3 seconds, updates the in_game_condition
def update_in_game_condition(in_game_condition):
    threading.Timer(3.0, update_in_game_condition, args=[in_game_condition]).start()
    is_in_game = check_website_in_game()
    if is_in_game:
        in_game_condition.set()
        print("checked - in game")
    else:
        in_game_condition.clear()
        print("checked - not in game")


def new_match_button():
    try:
        return driver.find_element(By.CLASS_NAME,'ui_v5-button-icon.icon-font-chess.plus')
    except:
        return None

def startup():
    hit_play()
    set_level()
    play_as_guest()
    change_to_bullet()
    find_match()



# should only be called once the game starts
def play_game(clicker, engine, color, in_game_condition):

    move_count = 1

    if color == 'black':
        opponent_move = get_move(move_count, in_game_condition)

        if opponent_move is None:
            return

        print("white move: " + opponent_move)
        engine.process_move(opponent_move)
        move_count += 1

    # new match button = ui_v5-button-component ui_v5-button-basic

    #while (no new match button):
    while in_game_condition.is_set():
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

        p1_move = get_move(move_count, in_game_condition)

        if p1_move is None:
            return

        # print(p1 + " move: " + p1_move)
        engine.process_move(p1_move)
        move_count += 1

        if p2 == color:
            uci, san = engine.get_engine_move()
            # print("suggested move: " + san)
            clicker.make_move(uci, san)

        p2_move = get_move(move_count, in_game_condition)
        if p2_move is None:
            return
        # print(p2 + " move: " + p2_move)
        engine.process_move(p2_move)
        move_count += 1


def wait_for_rematch(seconds, in_game_condition):

    for _ in range(seconds):

        if in_game_condition.is_set():
            return 'INGAME'  
        
        try:
            rematch_element = driver.find_element(By.CLASS_NAME, 'ui_v5-button-icon.icon-font-chess.checkmark')
            return rematch_element
        except:
            time.sleep(1)

    return None



# play entire thing
def play():
    
    engine = Engine()
    clicker = Clicker(driver, None)
    in_game_condition = Event()
    
    # updates every 3 seconds
    update_in_game_condition(in_game_condition)

    while True:
        #print("play loop")
        if in_game_condition.is_set():
            
            # delay between other thread interrupting and main thread continuing here

            print("in game condition set")
            # play game
            color, opponent_color = get_color()
            print("your color: " + color)
            clicker.set_color(color)
            clicker.initialize_sizes()
            engine.reset()
            play_game(clicker, engine, color, in_game_condition)
        else:
            
            print("game over or looking...")
            # game is over or looking for game
            new_match_element = new_match_button()
            
            if new_match_element is not None:
                print("there is a new match button!")
                # if new match button, means game is over

                # see if dude wants rematch
                rematch_element = wait_for_rematch(7, in_game_condition)

                if rematch_element == 'INGAME':
                    continue
                elif rematch_element is not None:
                    rematch_element.click()
                else:
                    try:
                        new_match_element = new_match_button()
                        new_match_element.click()
                    except:
                        print("an exception occurred while trying to hit the new match element")
                        continue
                    
                # try:
                #     print("waiting for rematch button...")
                #     if not in_game_condition.is_set():
                #         rematch_element = WebDriverWait(driver, timeout=7).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui_v5-button-icon.icon-font-chess.checkmark')))
                #         # hit rematch button
                #         rematch_element.click()
                #         print("rematch!")
                # except:
                #     print("no rematch button found after 7 seconds, hit new game!")
                #     # too long, don't rematch, hit new game
                #     # hacky fix
                #     try:
                #         #new_match_element.click()
                #         new_match_element = new_match_button()
                #         new_match_element.click()

                #     except:
                #         print("an exception occurred while trying to hit the new match element")
                #         continue
            
            else:
                print("no new match element found")
                continue


startup()
play()
