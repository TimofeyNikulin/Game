import math


# setting of game
HEIGHT = 800
WIDTH = 1200
MAP_SIZE = 8
TILE = int(WIDTH / 10 / 2)
FPS = 80
number_of_level = 0

# player
SPEED = 3

# texture
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# ray casting
MAX_DEPTH = 800
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 300
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = WIDTH / CASTED_RAYS
DIST = CASTED_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE

# sprite settings
DOUBLE_PI = math.pi * 2
CENTER_RAY = CASTED_RAYS // 2 - 1

# Minimap
MAP_SCALE = 5
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (1200, 0)
