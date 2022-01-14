from functions import *
from main_game import *
import pygame

class Board:
    global width, height, screen
    def __init__(self):
        self.weight = width
        self.height = height
        self.height1 = 1300
        self.display = screen
        self.board = load_image("board.jpg")
        self.pos_board = self.board.get_rect(center=(self.weight // 2, self.height // 2))
        self.display.blit(self.board, self.pos_board)