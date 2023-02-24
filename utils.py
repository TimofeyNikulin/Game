from levels import LEVELS
from config import *
import pygame
import math


class Field:
    def __init__(self):
        self.cell_size = TILE
        self.numberLevel = 0
        self.objectsOnLevel = []
        self.world_map = set()
        for j, row in enumerate(LEVELS[0]):
            for i, char in enumerate(row):
                if char == 'W':
                    self.world_map.add((i * MAP_TILE, j * MAP_TILE))

    def nextLevel(self):
        self.numberLevel += 1

    def draw(self, screen, screen_map, player_pos, player_angle):
        screen_map.fill((0, 0, 0))
        player_x, player_y = player_pos
        player_x //= MAP_SCALE
        player_y //= MAP_SCALE
        for x, y in self.world_map:
            pygame.draw.rect(screen_map, 'white',
                             (x, y, MAP_TILE, MAP_TILE))
        pygame.draw.circle(screen_map, (255, 0, 0),
                           (int(player_x), int(player_y)), 2)
        screen.blit(screen_map, MAP_POS)

        # pygame.draw.line(screen, (0,255,0),(player_x,player_y),(player_x - math.sin(player_angle) * 50,player_y + math.cos(player_angle) * 50),3)
        # pygame.draw.line(screen, (0,255,0),(player_x,player_y),(player_x - math.sin(player_angle - HALF_FOV) * 50,player_y + math.cos(player_angle - HALF_FOV) * 50),3)
        # pygame.draw.line(screen, (0,255,0),(player_x,player_y),(player_x - math.sin(player_angle + HALF_FOV) * 50,player_y + math.cos(player_angle + HALF_FOV) * 50),3)


class Player:
    def __init__(self, x=WIDTH / 2, y=HEIGHT / 2):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.angle = 0
        self.player_speed = SPEED

    def updatePos(self):
        self.pos = (self.x, self.y)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x += -self.player_speed * sin_a
            self.y += self.player_speed * cos_a
        if keys[pygame.K_a]:
            self.x += self.player_speed * sin_a
            self.y += -self.player_speed * cos_a
        if keys[pygame.K_w]:
            self.x += self.player_speed * cos_a
            self.y += self.player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -self.player_speed * cos_a
            self.y += -self.player_speed * sin_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.03
        if keys[pygame.K_RIGHT]:
            self.angle += 0.03
        self.updatePos()
        # print(self.x, self.y)


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.world_map = set()
        for j, row in enumerate(LEVELS[0]):
            for i, char in enumerate(row):
                if char == 'W':
                    self.world_map.add((i * TILE, j * TILE))

    def coordOfSquare(self, x, y):
        return (x // TILE) * TILE, (y // TILE) * TILE

    def ray_casting(self, player_pos, player_angle, texture):
        start_angle = player_angle - HALF_FOV
        player_x, player_y = player_pos
        square_x, square_y = self.coordOfSquare(player_x, player_y)
        for ray in range(CASTED_RAYS):
            sin_a = math.sin(start_angle)
            cos_a = math.cos(start_angle)

            x, dx = (square_x + TILE, 1) if cos_a >= 0 else (square_x, -1)
            for i in range(0, WIDTH, TILE):
                depth_v = (x - player_x) / cos_a
                yv = player_y + depth_v * sin_a
                if self.coordOfSquare(x + dx, yv) in self.world_map:
                    break
                x += dx * TILE

            y, dy = (square_y + TILE, 1) if sin_a >= 0 else (square_y, -1)
            for i in range(0, HEIGHT, TILE):
                depth_h = (y - player_y) / sin_a
                xh = player_x + depth_h * cos_a
                if self.coordOfSquare(xh, y + dy) in self.world_map:
                    break
                y += dy * TILE

            depth, offset = (
                depth_v, yv) if depth_v < depth_h else (depth_h, xh)
            offset = int(offset) % TILE
            depth *= math.cos(player_angle - start_angle)
            depth = max(depth, 0.00001)
            proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)
            wall_column = texture.subsurface(
                offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(
                wall_column, (SCALE, proj_height))
            self.screen.blit(
                wall_column, (ray * SCALE, HEIGHT // 2 - proj_height // 2))
            start_angle += STEP_ANGLE

    def world(self):
        pygame.draw.rect(self.screen, (55, 55, 55),
                         (0, HEIGHT / 2, WIDTH, HEIGHT))
        pygame.draw.rect(self.screen, (55, 55, 55),
                         (0, -HEIGHT / 2, WIDTH, HEIGHT))
