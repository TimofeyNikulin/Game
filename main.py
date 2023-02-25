import pygame
from config import *
from levels import LEVELS
from utils import Field, Player, Map
# from startPage import start_screen


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    screen = pygame.display.set_mode((WIDTH + 240, HEIGHT))
    clock = pygame.time.Clock()
    # start_screen(screen, clock)
    textures = {'1': pygame.image.load('img/1.png').convert(),
                '2': pygame.image.load('img/2.png').convert(),
                'key': pygame.image.load('img/key.png').convert()}
    screen_map = pygame.Surface(
        (WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE - 40))
    running = True
    player = Player()
    field = Field()
    map = Map(screen)
    map.draw_inventory()
    while running:
        player.movement()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        map.world()
        map.ray_casting(player.pos, player.angle, textures)
        field.draw(screen, screen_map, player.pos, player.angle)
        clock.tick(FPS)
        print(clock.get_fps())

        pygame.display.update()

pygame.quit()
