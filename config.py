import math


# setting of game
HEIGHT = 480
WIDTH = HEIGHT * 2
MAP_SIZE = 8
TILE = int(WIDTH / 10 / 2)
FPS = 80

# player
SPEED = 2

# ray casting
MAX_DEPTH = 800
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 300
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = WIDTH / CASTED_RAYS
DIST = CASTED_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE

# Minimap
MAP_SCALE = 5
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)