import sys
import pygame
from config import *


def terminate():
    pygame.quit()
    sys.exit()


def end_screen(screen, clock):
    screen.fill((0, 0, 0))
    intro_text = ["Поздравляем!", "Вы прошли лабиринт"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)
