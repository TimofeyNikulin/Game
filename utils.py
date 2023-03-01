from levels import LEVELS
from config import *
import pygame
import math
from endPage import end_screen


def reload(screen, map, field, fourKeys):
    sprites = Sprites()
    player = Player(screen=screen, sprites=sprites,
                    amount_keys=0)
    field = Field()
    map = Map(screen)
    map.draw_inventory()
    fourKeys = False
    player.map = map
    player.field = field


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'key': pygame.image.load('img/sprites/1.png').convert()
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['key'],
                         True, (12.5, 8.5), 1.8, 0.4),
            SpriteObject(self.sprite_types['key'], True, (1.5, 8.5), 1.8, 0.4),
            SpriteObject(self.sprite_types['key'], True, (2.5, 1.5), 1.8, 0.4),
            SpriteObject(self.sprite_types['key'], True, (7.5, 6.5), 1.8, 0.4)
        ]

    def reload(self):
        self.__init__()


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale
        self.side = 30
        self.pos = self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player, walls):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx**2 + dy**2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / STEP_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * STEP_ANGLE)

        if 0 <= current_ray <= CASTED_RAYS - 1 and distance_to_sprite < walls[current_ray][0]:
            proj_height = int(PROJ_COEFF / distance_to_sprite * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            sprite_pos = (current_ray * SCALE - half_proj_height,
                          HEIGHT // 2 - half_proj_height + shift)
            sprite = pygame.transform.scale(
                self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False, )

    def reload(self):
        self.__init__()


class Field:
    def __init__(self):
        self.cell_size = TILE
        self.numberLevel = 0
        self.objectsOnLevel = []
        self.world_map = set()
        for j, row in enumerate(LEVELS[number_of_level]):
            for i, char in enumerate(row):
                if char == '1' or char == '2' or char == 'D':
                    self.world_map.add((i * MAP_TILE, j * MAP_TILE))

    def nextLevel(self):
        self.numberLevel += 1

    def reload(self):
        self.__init__()

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


class Player:
    def __init__(self, screen, sprites, amount_keys, clock, x=WIDTH / 2, y=HEIGHT / 2):
        self.sprites = sprites
        self.sprites_for_reload = sprites
        self.amount_keys = amount_keys
        self.pos = self.x, self.y = x, y
        self.clock = clock
        self.angle = 0
        self.player_speed = SPEED
        self.collision_walls = []
        self.side = 20
        self.screen = screen
        self.rect = pygame.Rect(*self.pos, self.side, self.side)
        self.collision_sprites = [pygame.Rect(
            *obj.pos, obj.side, obj.side) for obj in self.sprites.list_of_objects if obj.static]
        self.door = 0
        self.map = ''
        self.field = ''
        self.spriteObject = ''
        for j, row in enumerate(LEVELS[number_of_level]):
            for i, char in enumerate(row):
                if char != ' ':
                    if char == 'D':
                        self.door = len(self.collision_walls)
                    self.collision_walls.append(
                        pygame.Rect(i * TILE, j * TILE, TILE, TILE))
        self.collision_list = self.collision_walls + self.collision_sprites

    def updatePos(self):
        self.pos = (self.x, self.y)

    def reload(self):
        self.__init__(screen=self.screen, sprites=self.sprites,
                      amount_keys=4, clock=self.clock)

    def addKey(self):
        key_pos_list = [(1206, 126), (1324, 126), (1206, 225), (1324, 225)]
        self.amount_keys -= 1
        pos = key_pos_list[self.amount_keys]
        pygame.draw.rect(self.screen, 'yellow',
                         (pos[0], pos[1], 110, 90))

    def detect_collision(self, dx, dy):
        global number_of_level
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)
        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                if self.collision_list[hit_index] in self.collision_list[-4:]:
                    object = self.collision_list[hit_index]
                    for obj in self.sprites.list_of_objects:
                        print(obj.pos, (object.left, object.top))
                        if obj.pos == (object.left, object.top):
                            self.sprites.list_of_objects.pop(
                                self.sprites.list_of_objects.index(obj))
                            self.collision_list.pop(hit_index)
                            self.addKey()
                    continue
                if hit_index == self.door and self.amount_keys == 0:
                    number_of_level += 1
                    if number_of_level == 3:
                        end_screen(self.screen, self.clock)
                    self.map.reload()
                    self.field.reload()
                    self.sprites.reload()
                    map = self.map
                    field = self.field
                    sprites = self.spriteObject
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (1200, 120, 240, 201))
                    map.draw_inventory()
                    self.reload()
                    self.field = field
                    self.map = map
                    self.spriteObject = sprites

                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            dx = -self.player_speed * sin_a
            dy = self.player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = self.player_speed * sin_a
            dy = -self.player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_w]:
            dx = self.player_speed * cos_a
            dy = self.player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -self.player_speed * cos_a
            dy = -self.player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.03
        if keys[pygame.K_RIGHT]:
            self.angle += 0.03
        self.rect.center = self.x, self.y
        self.updatePos()
        # print(self.x, self.y)
        self.angle %= DOUBLE_PI


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.world_map = {}
        for j, row in enumerate(LEVELS[number_of_level]):
            for i, char in enumerate(row):
                if char == '1':
                    self.world_map[(i * TILE, j * TILE)] = '1'
                elif char == '2':
                    self.world_map[(i * TILE, j * TILE)] = '2'
                elif char == 'D':
                    self.world_map[(i * TILE, j * TILE)] = 'door'

    def coordOfSquare(self, x, y):
        return (x // TILE) * TILE, (y // TILE) * TILE

    def reload(self):
        self.__init__(self.screen)

    def ray_casting(self, player, textures, fourKeys):
        walls = []
        start_angle = player.angle - HALF_FOV
        player_x, player_y = player.pos
        square_x, square_y = self.coordOfSquare(player_x, player_y)
        for ray in range(CASTED_RAYS):
            sin_a = math.sin(start_angle)
            cos_a = math.cos(start_angle)
            x, dx = (square_x + TILE, 1) if cos_a >= 0 else (square_x, -1)
            for i in range(0, WIDTH, TILE):
                depth_v = (x - player_x) / cos_a
                yv = player_y + depth_v * sin_a
                tile_v = self.coordOfSquare(x + dx, yv)
                if tile_v in self.world_map.keys():
                    texture_v = textures[
                        self.world_map[tile_v]]
                    if self.world_map[tile_v] == 'door' and fourKeys != True:
                        texture_v = texture_v[0]
                    elif self.world_map[tile_v] == 'door' and fourKeys == True:
                        texture_v = texture_v[1]
                    break
                x += dx * TILE

            y, dy = (square_y + TILE, 1) if sin_a >= 0 else (square_y, -1)
            for i in range(0, HEIGHT, TILE):
                depth_h = (y - player_y) / sin_a
                xh = player_x + depth_h * cos_a
                tile_h = self.coordOfSquare(xh, y + dy)
                if tile_h in self.world_map.keys():
                    texture_h = textures[
                        self.world_map[tile_h]]
                    if self.world_map[tile_h] == 'door' and fourKeys != True:
                        texture_h = texture_h[0]
                    elif self.world_map[tile_h] == 'door' and fourKeys == True:
                        texture_h = texture_h[1]
                    break
                y += dy * TILE

            depth, offset, texture = (
                depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
            offset = int(offset) % TILE
            depth *= math.cos(player.angle - start_angle)
            depth = max(depth, 0.00001)
            proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)
            wall_column = texture.subsurface(
                offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(
                wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HEIGHT // 2 - proj_height // 2)

            walls.append((depth, wall_column, wall_pos))
            start_angle += STEP_ANGLE

        return walls

    def world(self, world_objects):
        pygame.draw.rect(self.screen, (55, 55, 55),
                         (0, HEIGHT / 2, WIDTH, HEIGHT))
        pygame.draw.rect(self.screen, (55, 55, 55),
                         (0, -HEIGHT / 2, WIDTH, HEIGHT))
        pygame.draw.rect(self.screen, (30, 30, 30),
                         (1200, 320, 240, HEIGHT - 320))
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

    def draw_inventory(self):
        pygame.draw.line(self.screen, (100, 100, 100),
                         (1200, 220), (1440, 220), 5)
        pygame.draw.line(self.screen, (100, 100, 100),
                         (1320, 120), (1320, 320), 5)
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (1200, 120, 240, 201), 5)
