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
  # print(f'x={x}')
  lines[x] = [lines[x][0], int(lines[x][1:])]

# for line in lines:
#   print(line)
print(f'Loaded {len(lines)} lines.')

waypoint = [10, 1]
location = [0, 0]


def move_waypoint(waypoint, direction, amount):
  if direction == 'N':
    waypoint[1] += amount
  if direction == 'E':
    waypoint[0] += amount
  if direction == 'S':
    waypoint[1] -= amount
  if direction == 'W':
    waypoint[0] -= amount

  return waypoint


def move_to_waypoint(waypoint, location, times):
  location[0] += (waypoint[0] * times)
  location[1] += (waypoint[1] * times)

  return location


def rotate_waypoint(waypoint, direction, degrees):
  if (direction == 'R' and degrees == 90) or (direction == 'L' and degrees == 270):
    # 90 clockwise
    newX = waypoint[1]
    newY = waypoint[0] * -1
  elif degrees == 180:
    newX = waypoint[0] * -1
    newY = waypoint[1] * -1
  elif (direction == 'R' and degrees == 270) or (direction == 'L' and degrees == 90):
    newX = waypoint[1] * -1
    newY = waypoint[0]

  waypoint[0] = newX
  waypoint[1] = newY

  return waypoint


for line in lines:
  if line[0] == 'F':
    location = move_to_waypoint(waypoint, location, int(line[1]))
  elif line[0] in ['L', 'R']:
    waypoint = rotate_waypoint(waypoint, line[0], int(line[1]))
  else:
    waypoint = move_waypoint(waypoint, line[0], int(line[1]))

  print(f'Command: {line}, waypoint: {waypoint}, location: {location}')

print(f'X={location[0]}, y={location[1]}; manhattan distance = {abs(location[0]) + abs(location[1])}')
