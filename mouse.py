from selenium.webdriver.common.by import By
from selenium import webdriver
import random
emojis = [
'laugh', 'kiss', 'strong', 'tongue', 'star', 'evil', 'grin'
]


class Clicker:

    def __init__(self, driver, color):
        self.driver = driver
        self.color = color
    
    def initialize_sizes(self):
        if self.color == 'white':
            e = self.driver.find_element(By.CLASS_NAME, "piece.wr.square-11")
        else:
            e = self.driver.find_element(By.CLASS_NAME, "piece.br.square-88")

        self.square_size = e.size['width']
        self.bottom_right_x = e.location['x'] + e.size['width'] / 2
        self.bottom_right_y = e.location['y'] + e.size['width'] / 2
        self.gear = self.driver.find_element(By.CLASS_NAME, "board-layout-icon.icon-font-chess.circle-gearwheel")
        self.gear_x = self.gear.location['x'] + self.gear.size['width'] / 2
        self.gear_y = self.gear.location['y'] + self.gear.size['height'] / 2

    def get_origin_square_element_castle(self, color):
        
        prefix = "piece." + color[0] + "k.square-"

        if color == 'white':
            prefix += '51'
        else:
            prefix += '58'

        return self.driver.find_element(By.CLASS_NAME, prefix)

    # given uci (g2g4) and san(Nf4), return the origin sqaure from chess so the 
    # mouse knows where to click
    def get_origin_square_element(self, uci, san, color):

        if san == 'O-O' or san == 'O-O-O':
            return self.get_origin_square_element_castle(color)

        piece = 'p'

        if san[0].isupper():
            piece = san[0].lower()
        
        origin_col_letter = uci[0]
        origin_col = ord(origin_col_letter) - 96

        origin_row = uci[1]
        #print("uci: " + uci)
        #print("origin row: " + str(origin_row))
        class_name =  "piece." + color[0] + piece + ".square-" + str(origin_col) + str(origin_row)
        return self.driver.find_element(By.CLASS_NAME, class_name)

    def move_to_board(self):
        board_element = self.driver.find_element(By.CLASS_NAME, 'board')
        webdriver.ActionChains(self.driver).move_to_element(board_element).perform()

    
    def uci_square_to_coordinate(self, col_letter, row):

        col = ord(col_letter) - 97
        row = int(row) - 1

        # 0 based indexing

        if self.color == 'white':

            x = self.bottom_right_x + self.square_size * col
            y = self.bottom_right_y - self.square_size * row
        else:
            x = self.bottom_right_x + self.square_size * (7 - col)
            y = self.bottom_right_y - self.square_size * (7 - row)

        return x, y

    def click_coordinate(self, x, y, times):
        action = webdriver.common.action_chains.ActionChains(self.driver)
        action.move_to_element_with_offset(self.gear, x - self.gear_x, y - self.gear_y)
        
        for _ in range(times):
            action.click()
            action.perform()

    def click_origin(self, uci):
        
        x, y = self.uci_square_to_coordinate(uci[0], uci[1])
        self.click_coordinate(x, y, 1)


    def click_destination(self, uci, san):
        
        x, y = self.uci_square_to_coordinate(uci[2], uci[3])
  
        # promote
        if '=' in san:
            self.click_coordinate(x, y, 2)
        else:
            self.click_coordinate(x, y, 1)

    def make_move(self, uci, san):
        self.click_origin(uci)
        self.click_destination(uci, san)

    def emoji(self):
        try:
            message_button = self.driver.find_element(By.CLASS_NAME, "emoticons-popup-button")
            message_button.click()
            random_emoji = random.choice(emojis)
            emoji = self.driver.find_element(By.CLASS_NAME, "emoticon-select.emoticon-select-" + random_emoji)
            emoji.click()
        except:
            return

# top right rook x offset = gear_x 