import pygame
from consts import *
from start_screen import *

sc = Start_Screen()
begining = Vibor_igrokov()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
