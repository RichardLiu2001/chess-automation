from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
from threading import Event
import time
from Engine import Engine
from mouse import Clicker
from StatTracker import StatTracker

chess_url = "https://www.chess.com"

class FireFoxPlayer:

    def __init__(self, my_moves=0, stockfish_moves=1, stockfish_level=3000):

        self.driver = webdriver.Firefox()
        self.driver.get(chess_url)
        self.engine = Engine()

    def get_result_of_game(self):

        result_text = self.driver.find_element (By.CLASS_NAME, "header-title-component").text

        result = 'win'
        if "White" in result_text or "Black" in result_text:
            result = "loss"
        
        if "Draw" in result_text:
            result = 'draw'

        if "Aborted" in result_text:
            result = 'abort'

        by = self.driver.find_element (By.CLASS_NAME, "header-subtitle-component").text

        opponent = self.driver.find_elements(By.CLASS_NAME, "user-username-component.user-username-dark.user-username-link.user-tagline-username")[0].text

        return result, by, opponent


    def hit_play(self):
        play_online_button = self.driver.find_element(By.CLASS_NAME, "index-guest-button.ui_v5-button-component.ui_v5-button-large.ui_v5-button-primary.ui_v5-button-full")
        play_online_button.click()


    def play_as_guest(self):
        guest_button = self.driver.find_element(By.ID, "guest-button")
        guest_button.click() 


    def change_to_bullet(self):
        change_time_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-font-chess.chevron-bottom.time-selector-chevron')))
        change_time_button.click()
        bullet_button = self.driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-basic.ui_v5-button-small.ui_v5-button-full.time-selector-category-btn")
        bullet_button.click()


    def set_level(self, level='Advanced'):
        level_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='" + level + "']")))
        level_button.click()
        level_button.click()


    def find_match(self):
        play_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")))
        #play_button = driver.find_element(By.CLASS_NAME, "ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")
        play_button.click()


    def wait_game_start(self):
        # wait for draw button to appear
        WebDriverWait(self.driver, float('inf')).until(EC.presence_of_element_located((By.CLASS_NAME, "draw-button-label")))


    def get_color(self):
        color = "black"
        opponent_color = 'white'

        found_color = False
        while not found_color:
            try:
                self.driver.find_element(By.CLASS_NAME, "clock-component.clock-black.clock-bottom.clock-live.clock-running.player-clock.clock-player-turn")
                found_color = True
            except:
                try:
                    self.driver.find_element(By.CLASS_NAME, "clock-component.clock-black.clock-top.clock-live.clock-running.player-clock")
                    found_color = True
                    color = "white"
                    opponent_color = 'black'
                except:
                    continue
        return color, opponent_color


    def wait_move(self, move_count, in_game_condition):
        # return text of opponent move
        
        while in_game_condition.is_set():
            try:
                return self.driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']')
            except:
                continue
        
        # game ended before a move was made
        return None


    def get_move(self, move_count, in_game_condition):
        piece = None
        try:
            move_element = self.driver.find_element(by=By.XPATH, value='//div[@data-ply=' + '"' + str(move_count) + '"' + ']').text
            try:
                piece_element = move_element.find_element(by=By.XPATH, value=".//*")
                piece = piece_element.get_attribute("data-figurine")
            except:
                piece = ""
            if piece == None:
                piece = ""
            return piece + move_element.text
        except:
            move_element = self.wait_move(move_count, in_game_condition)
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


    def check_website_in_game(self):
        try:
            # if there is the draw button, you are in a game
            self.driver.find_element(By.CLASS_NAME, "draw-button-label")
            return True
        except:
            return False


    # runs every 3 seconds, updates the in_game_condition
    def update_in_game_condition(self, in_game_condition):
        threading.Timer(3.0, self.update_in_game_condition, args=[in_game_condition]).start()
        is_in_game = self.check_website_in_game()
        if is_in_game:
            in_game_condition.set()
            #print("checked - in game")
        else:
            in_game_condition.clear()
            #print("checked - not in game")


    def new_match_button(self):
        try:
            return self.driver.find_element(By.CLASS_NAME,'ui_v5-button-icon.icon-font-chess.plus')
        except:
            return None


    def startup(self):
        self.hit_play()
        self.set_level()
        self.play_as_guest()
        self.change_to_bullet()
        self.find_match()


    # should only be called once the game starts
    def play_game(self, clicker, color, in_game_condition):

        move_count = 1

        if color == 'black':
            opponent_move = self.get_move(move_count, in_game_condition)

            if opponent_move is None:
                return

            self.engine.process_move(opponent_move)
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
                uci, san = self.engine.get_engine_move()
                #clicker.highlight_move(uci)
                clicker.make_move(uci, san)
                #clicker.drag_and_drop_move(uci, san)

            p1_move = self.get_move(move_count, in_game_condition)

            if p1_move is None:
                return

            self.engine.process_move(p1_move)
            move_count += 1

            if p2 == color:
                uci, san = self.engine.get_engine_move()
                #clicker.highlight_move(uci)
                clicker.make_move(uci, san)
                #clicker.drag_and_drop_move(uci, san)

            p2_move = self.get_move(move_count, in_game_condition)
            if p2_move is None:
                return
            self.engine.process_move(p2_move)
            move_count += 1


    def wait_for_rematch(self, seconds, in_game_condition):

        for _ in range(2 * seconds):

            if in_game_condition.is_set():
                return 'INGAME'  
            
            try:
                rematch_element = self.driver.find_element(By.CLASS_NAME, 'ui_v5-button-icon.icon-font-chess.checkmark')
                return rematch_element
            except:
                time.sleep(.5)

        return None

    def login(self, username, password):

    # driver = webdriver.Firefox()
    # chess_url = "https://www.chess.com"
    # driver.get(chess_url)

        login_button = self.driver.find_element(by=By.CLASS_NAME, value='button.auth.login.ui_v5-button-component.ui_v5-button-primary')
        login_button.click()

        username_form = self.driver.find_element(by=By.ID, value="username")
        username_form.send_keys(username)

        password_form = self.driver.find_element(by=By.ID, value="password")
        password_form.send_keys(password)

        login = self.driver.find_element(By.ID, 'login')
        login.click()

        modal_x = self.driver.find_element(By.CLASS_NAME, 'icon-font-chess.x.ui_outside-close-icon')
        modal_x.click()

        new_game = self.driver.find_element(By.ID, 'quick-link-new_game')
        new_game.click()

        self.change_to_bullet()
        self.find_match()

    # play entire thing
    def play(self):
        
        clicker = Clicker(self.driver, None)
        stat_tracker = StatTracker()
        in_game_condition = Event()
        
        # updates every 3 seconds
        self.update_in_game_condition(in_game_condition)

        while True:
            if in_game_condition.is_set():
                
                # delay between other thread interrupting and main thread continuing here
                #print("in game condition set")
                color, opponent_color = self.get_color()
                #print("your color: " + color)
                clicker.set_color(color)
                clicker.initialize_sizes()
                self.engine.reset()
                self.play_game(clicker, self.engine, color, in_game_condition)
            else:
                
                #print("game over or looking...")
                # game is over or looking for game
                new_match_element = self.new_match_button()
                
                if new_match_element is not None:
                    #print("there is a new match button!")
                    # if new match button, means game is over

                    # collect data
                    try:
                        result, by, opponent = self.get_result_of_game()
                        stat_tracker.update(result, by, opponent)
                        stat_tracker.print_stats()
                    except:
                        pass

                    # see if dude wants rematch
                    rematch_element = self.wait_for_rematch(7, in_game_condition)

                    if rematch_element == 'INGAME':
                        continue
                    elif rematch_element is not None:
                        print("rematch!")
                        rematch_element.click()
                    else:
                        
                        if in_game_condition.is_set():
                            continue

                        try:
                            new_match_element = self.new_match_button()
                            new_match_element.click()
                        except:
                            #print("an exception occurred while trying to hit the new match element")
                            continue
                
                else:
                    #print("no new match element found")
                    continue



fireFoxPlayer = FireFoxPlayer()
fireFoxPlayer2 = FireFoxPlayer()

fireFoxPlayer.startup()

fireFoxPlayer2.startup()

fireFoxPlayer.play()
fireFoxPlayer2.play()
