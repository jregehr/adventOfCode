import re
import sys
import csv
import copy
import math

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file, 'r') as f:
  contents = f.read()

lines = re.split('\n', contents)

for x in range(len(lines)):
  print(f'x={x}')
  lines[x] = [lines[x][0], int(lines[x][1:])]

# for line in lines:
#   print(line)
print(f'Loaded {len(lines)} lines.')

location = [90, 0, 0]


def move(distance, location):
  if location[0] == 90:
    location[1] += distance
  elif location[0] == 270:
    location[1] -= distance
  elif location[0] == 180:
    location[2] -= distance
  elif location[0] == 0:
    location[2] += distance

  return location


def move_dir(direction, distance, location):
  if direction == 'N':
    location[2] += distance
  elif direction == 'S':
    location[2] -= distance
  elif direction == 'W':
    location[1] -= distance
  elif direction == 'E':
    location[1] += distance

  return location


def turn(direction, amount, location):
  theAmount = amount
  if direction == 'L':
    theAmount = -1 * amount

  location[0] += theAmount

  if location[0] < -359 or location[0] > 359:
    location[0] = location[0] % 360

  if location[0] < 0:
    location[0] += 360

  return location


for line in lines:
  if line[0] == 'F':
    location = move(line[1], location)
  elif line[0] == 'L' or line[0] == 'R':
    location = turn(line[0], line[1], location)
  else:
    location = move_dir(line[0], line[1], location)

  print(location)

print(f'Facing {location[0]}, x={location[1]}, y={location[2]}; manhattan distance = {abs(location[1]) + abs(location[2])}')
