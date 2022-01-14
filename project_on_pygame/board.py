from functions import *
from consts import *
import pygame

class Board:
    def __init__(self):
        self.weight = size[0]
        self.height = size[1]
        self.height1 = 1300
        self.display = screen
        self.board = load_image("board.jpg")
        self.pos_board = self.board.get_rect(center=(self.weight // 2, self.height // 2))
        self.display.blit(self.board, self.pos_board)