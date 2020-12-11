import re
import sys
import csv
import copy
import math

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [list(line.strip()) for line in f]

# for line in lines:
#   print(line)
print(f'Loaded {len(lines)} lines.')

# lines2 = copy.deepcopy(lines)

# if lines == lines2:
#   print('after deep copy - The patterns are equal')
# else:
#   print('after deep copy - not equal')

# lines2[3][4] = 'X'

# if lines == lines2:
#   print('after edit - The patterns are equal')
# else:
#   print('after edit - not equal')

# for line in lines:
#   print(line)
# print('lines2')
# for line in lines2:
#   print(line)


def get_surrounding(waiting_area, x, y):
  surroundings = ''
  for ys in range(max(0, y-1), min(y+2, len(waiting_area))):
    for xs in range(max(0, x-1), min(x+2, len(waiting_area[0]))):
      if xs == x and ys == y:
        continue
      surroundings += waiting_area[ys][xs]
  # print(f'Debug: x{x}, y{y}, surroundings={surroundings}')
  return surroundings


def should_occupy(waiting_area, x, y):
  occupied = waiting_area[y][x]
  if occupied == "L":
    # empty seat
    if get_surrounding(waiting_area, x, y).count('#') == 0:
      return "#"

  if occupied == "#":
    # occupied seat
    if get_surrounding(waiting_area, x, y).count('#') >= 4:
      return "L"

  return occupied


def get_occupied(waiting_area):
  occupied = 0
  for line in waiting_area:
    for seat in line:
      if seat == "#":
        occupied += 1

  return occupied


round = 0
current = lines
future = copy.deepcopy(lines)

while True:
  round += 1
  for y in range(0, len(current)):
    for x in range(0, len(current[0])):
      future[y][x] = should_occupy(current, x, y)

  print(f'After round {round}, {get_occupied(future)} occupied seats:')
  # for line in future:
  #   print(line)

  if current == future:
    print(f'After {round} rounds no changes were made.')
    break

  current = copy.deepcopy(future)
