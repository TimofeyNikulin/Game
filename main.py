import pygame
from config import *
from levels import LEVELS
from utils import Field, Player, Map, Sprites, SpriteObject
from startPage import start_screen


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    screen = pygame.display.set_mode((WIDTH + 240, HEIGHT))
    clock = pygame.time.Clock()
    start_screen(screen, clock)
    textures = {'1': pygame.image.load('img/1.png').convert(),
                '2': pygame.image.load('img/2.png').convert(),
                'door': [pygame.image.load('img/door.png').convert(), pygame.image.load('img/door2.png').convert()]}
    screen_map = pygame.Surface(
        (WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE - 40))
    running = True
    player = Player()
    field = Field()
    map = Map(screen)
    sprites = Sprites()
    map.draw_inventory()
    fourKeys = False
    while running:
        player.movement()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        walls = map.ray_casting(player, textures, fourKeys)
        map.world(walls + [obj.object_locate(player, walls)
                  for obj in sprites.list_of_objects])
        field.draw(screen, screen_map, player.pos, player.angle)
        clock.tick(FPS)
        print(clock.get_fps())

        pygame.display.update()

pygame.quit()
