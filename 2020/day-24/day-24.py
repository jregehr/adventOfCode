import re
import sys
import csv
import math
import copy
from collections import Counter

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

# print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

# print(lines)
print(f'Loaded {len(lines)} lines.')


#region Debug Printers

def debug_print(phase, output):
  if debug <= phase:
    print(output)


LINE_BREAK = '================================================'


def debug_line_break(phase):
  debug_print(phase, LINE_BREAK)

#endregion


##############################################
debug = 2
##############################################

#region Classes


class Tile:
  COLOR_BLACK = 'black'
  COLOR_WHITE = 'white'
  DIRECTION_E = 'e'
  DIRECTION_SE = 'se'
  DIRECTION_SW = 'sw'
  DIRECTION_W = 'w'
  DIRECTION_NE = 'ne'
  DIRECTION_NW = 'nw'
  DIRECTIONS = [DIRECTION_E, DIRECTION_SE, DIRECTION_SW, DIRECTION_W, DIRECTION_NE, DIRECTION_NW]

  def __init__(self, x, y):
    self._color = Tile.COLOR_WHITE
    self._x = x
    self._y = y

  def __str__(self):
    return f'Tile at {self._x},{self._y} has color {self._color}'

  def __repr__(self):
    return f'{self._x},{self._y}: {self._color}'

  @property
  def color(self):
    return self._color

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @property
  def coordinates(self):
    return f'{x}_{y}'

  def flip(self):
    if self._color == Tile.COLOR_WHITE:
      self._color = Tile.COLOR_BLACK
    else:
      self._color = Tile.COLOR_WHITE

  def get_surrounding_coordinates(self):
    # Return the following tiles:
    # E  - x+2, y
    # SE - x+1, y-1
    # SW - x-1, y-1
    # W  - x-2, y
    # NE - x+1, y+1
    # NW - x-1, y+1
    return [
        encodeCoordnate(self._x+2, self._y),
        encodeCoordnate(self._x+1, self._y-1),
        encodeCoordnate(self._x-1, self._y-1),
        encodeCoordnate(self._x-2, self._y),
        encodeCoordnate(self._x+1, self._y+1),
        encodeCoordnate(self._x-1, self._y+1)
    ]


#endregion

#region functions


def valid(direction):
  return direction in Tile.DIRECTIONS


def parse(line):
  debug_line_break(1)
  debug_print(1, f'Parsing {line}')
  result = []

  start = 0
  while True:
    chunk = line[start:start+2]
    if start == len(line) or chunk == '':
      break
    debug_print(1, f'Chunk={chunk}')
    if valid(chunk):
      result.append(chunk)
      start += 2
    elif valid(chunk[0:1]):
      result.append(chunk[0:1])
      start += 1
    else:
      debug_line_break(99)
      debug_print(99, f'I could not parse {chunk}')
      debug_line_break(99)
      sys.exit()

  return result


def living_art(tiles):
  new_tiles = {}
  to_flip = set(list(tiles.keys()))
  more_flip = check_and_flip(tiles, new_tiles, to_flip)
  check_and_flip(tiles, new_tiles, (more_flip - to_flip))
  return new_tiles


def check_and_flip(tiles, new_tiles, to_flip):
  more_flip = set()
  for coordinate in list(to_flip):
    tile_to_flip = get_tile_coord(tiles, coordinate)
    new_tile = copy.deepcopy(tile_to_flip)
    new_tiles[coordinate] = new_tile
    black_count = 0
    to_check = tile_to_flip.get_surrounding_coordinates()
    more_flip = more_flip | set(to_check)
    for coord in to_check:
      # more_flip.add(coord)
      if get_tile_coord(tiles, coord).color == Tile.COLOR_BLACK:
        black_count += 1
    if tile_to_flip.color == Tile.COLOR_WHITE and black_count == 2:
      new_tile.flip()
    elif tile_to_flip.color == Tile.COLOR_BLACK and (black_count == 0 or black_count > 2):
      new_tile.flip()
  return more_flip


def decodeCoordinate(coordinate):
  ## return x_y as x, y
  coordArray = coordinate.split('_')
  return int(coordArray[0]), int(coordArray[1])


def encodeCoordnate(x, y):
  return f'{x}_{y}'


def get_tile_coord(tiles, coordinate):
  tile = tiles.get(coordinate)
  if tile == None:
    x, y = decodeCoordinate(coordinate)
    tile = Tile(x, y)
    tiles[coordinate] = tile
  return tile


def get_tile_xy(tiles, x, y):
  return get_tile_coord(tiles, encodeCoordnate(x, y))


def flip(tiles, x, y):
  get_tile_xy(tiles, x, y).flip()


def move(direction, x, y):
  # y = current_y
  # x = current_x
  if direction == Tile.DIRECTION_E:
    return x+2, y
  elif direction == Tile.DIRECTION_SE:
    return x+1, y-1
  elif direction == Tile.DIRECTION_SW:
    return x-1, y-1
  elif direction == Tile.DIRECTION_W:
    return x-2, y
  elif direction == Tile.DIRECTION_NE:
    return x+1, y+1
  elif direction == Tile.DIRECTION_NW:
    return x-1, y+1
  else:
    debug_line_break(99)
    debug_print(99, f'I could not move in {direction}')
    debug_line_break(99)
    sys.exit()

#endregion

#region Data Loading


directionsets = []
for raw in lines:
  directionsets.append(parse(raw))

debug_print(1, 'starting values')
for directionset in directionsets:
  debug_print(1, directionset)

#endregion

tiles = {}
for directionset in directionsets:
  x = 0
  y = 0
  for direction in directionset:
    x, y = move(direction, x, y)
  flip(tiles, x, y)

debug_line_break(99)
print(f'Part 1: {Counter([tile.color for tile in tiles.values()])}')

for x in range(1, 101):
  tiles = living_art(tiles)
  if x < 10 or x % 10 == 0:
    print(f'Part 2, Day {x}: {Counter([tile.color for tile in tiles.values()])}')
