import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

print(lines)
print(f'Loaded {len(lines)} lines.')

# Constants
ACTIVE = '#'
INACTIVE = '.'
MIN_Z_ROW = 0
MIN_Y_ROW = 1
MIN_X_ROW = 2
MIN_W_ROW = 3
MIN_MIN = 0
MIN_MAX = 1


def decodeCoordinate(coordinate):
  ## return w_x_y_z as w, x, y, z
  coordArray = coordinate.split('_')
  return int(coordArray[0]), int(coordArray[1]), int(coordArray[2]), int(coordArray[3])


def encodeCoordnate(w, x, y, z):
  return f'{w}_{x}_{y}_{z}'


def loadSpace(lines):
  space = {}
  z = 0
  w = 0
  for y in range(len(lines)):
    for x in range(len(lines[y])):
      coord = encodeCoordnate(w, x, y, z)
      space[coord] = lines[y][x]
  return space, [
      [-1, 1],                # z
      [-1, len(lines)+1],     # y
      [-1, len(lines[0])+1],  # x
      [-1, 1]                 # w
  ]


def getCubeState(space, coordinate):
  if space.get(coordinate) == None:
    return INACTIVE
  return ACTIVE if space[coordinate] == ACTIVE else INACTIVE


def countActive(space, coordinate):  # , minMax):
  w, x, y, z = decodeCoordinate(coordinate)
  activeCount = 0
  # print(f'Start countActive for {coordinate}: {minMax}')
  for zz in range(z-1, z+2):
    for yy in range(y-1, y+2):
      for xx in range(x-1, x+2):
        for ww in range(w-1, w+2):
          # print(f'countActive z={zz}, y={yy}, x={xx}, {minMax}')
          # minMax[MIN_Z_ROW] = [min(zz, minMax[MIN_Z_ROW][MIN_MIN]), max(zz+1, minMax[MIN_Z_ROW][MIN_MAX])]
          # minMax[MIN_Y_ROW] = [min(yy, minMax[MIN_Y_ROW][MIN_MIN]), max(yy+1, minMax[MIN_Y_ROW][MIN_MAX])]
          # minMax[MIN_X_ROW] = [min(xx, minMax[MIN_X_ROW][MIN_MIN]), max(xx+1, minMax[MIN_X_ROW][MIN_MAX])]
          # don't count myself
          if w == ww and x == xx and y == yy and z == zz:
            continue
          if getCubeState(space, encodeCoordnate(ww, xx, yy, zz)) == ACTIVE:
            activeCount += 1
  # print(f'After countActive for {coordinate}: {minMax}')
  return activeCount  # , minMax


def cycle(space, minMax):
  newSpace = {}

  for z in range(minMax[MIN_Z_ROW][MIN_MIN]-1, minMax[MIN_Z_ROW][MIN_MAX]+1):
    for y in range(minMax[MIN_Y_ROW][MIN_MIN]-1, minMax[MIN_Y_ROW][MIN_MAX]+1):
      for x in range(minMax[MIN_X_ROW][MIN_MIN]-1, minMax[MIN_X_ROW][MIN_MAX]+1):
        for w in range(minMax[MIN_W_ROW][MIN_MIN]-1, minMax[MIN_W_ROW][MIN_MAX]+1):
          encoded = encodeCoordnate(w, x, y, z)
          # activeCount, minMax = countActive(space, encoded, minMax)
          activeCount = countActive(space, encoded)
          cubeState = getCubeState(space, encoded)
          newSpace[encoded] = cubeState
          if cubeState == ACTIVE:
            if activeCount not in [2, 3]:
              newSpace[encoded] = INACTIVE
          if cubeState == INACTIVE:
            if activeCount == 3:
              newSpace[encoded] = ACTIVE

  return newSpace


def countAllActive(space):
  activeCount = 0
  for coord in space.keys():
    if space[coord] == ACTIVE:
      activeCount += 1

  return activeCount


minMax = []
space = {}

space, minMax = loadSpace(lines)
print('=== after load =========================')
print(space)
print(minMax)
for x in range(0, 6):
  # space, minMax = cycle(space, minMax)
  space = cycle(space, minMax)
  # print(f'=== after cycle {x} =========================')
  print(f'Active Count after {x} cycles: {countAllActive(space)}')
  # print(space)
  minMax = [
      [minMax[MIN_Z_ROW][MIN_MIN]-1, minMax[MIN_Z_ROW][MIN_MAX]+1],
      [minMax[MIN_Y_ROW][MIN_MIN]-1, minMax[MIN_Y_ROW][MIN_MAX]+1],
      [minMax[MIN_X_ROW][MIN_MIN]-1, minMax[MIN_X_ROW][MIN_MAX]+1],
      [minMax[MIN_W_ROW][MIN_MIN]-1, minMax[MIN_W_ROW][MIN_MAX]+1],
  ]
  print(minMax)
