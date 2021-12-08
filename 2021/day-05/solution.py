import sys
import math

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  rawLines = f_input.readlines()

# print(lines)
print(f'Loaded {len(rawLines)} lines.')

#region Point Class

class Point:

  def __init__(self, pointString):
    xy = pointString.split(',')
    self._x = int(xy[0])
    self._y = int(xy[1])
  
  @property
  def x(self):
    return self._x
  
  @property
  def y(self):
    return self._y

  def greaterThan(self, point2):
    return self._x + self._y > point2.x + point2.y
  
  def length(self, point2):
    return math.sqrt((self._x - point2.x)**2 + (self._y - point2.y)**2)
  
  def __str__(self):
    return f'Point: {self._x},{self._y}'

#endregion

#region Line Class

class Line:

  def __init__(self, lineString):
    pointStrings = lineString.split(' ')
    p1 = Point(pointStrings[0])
    p2 = Point(pointStrings[2])

    if p2.greaterThan(p1):
      self._point1 = p1
      self._point2 = p2
    else:
      self._point1 = p2
      self._point2 = p1
  
  @property
  def isDiagonal(self):
    return self._point1.x != self._point2.x and self._point1.y != self._point2.y

  def passesThrough(self, x, y):
    passes = False
    if self.sameX and x == self._point1.x:
      if y <= max(self._point1.y, self._point2.y) and y >= min(self._point1.y, self._point2.y):
        passes = True
      
    if self.sameY and y == self._point1.y:
      if x <= max(self._point1.x, self._point2.x) and x >= min(self._point1.x, self._point2.x):
        passes = True

    # if (self._point1.x - x)*(self._point1.y - y) == (x - self._point2.x)*(y - self._point2.y):
    # if (x - self._point1.x) / (self._point2.x - self._point1.x) == (y - self._point1.y) / (self._point2.y - self._point1.y):
    pointc = Point(f'{x},{y}')
    p1pc = self._point1.length(pointc)
    pcp2 = pointc.length(self._point2)
    p1p2 = self._point1.length(self._point2)
    # print(f'p1pc={round(p1pc,3)}; pcp2={round(pcp2, 3)}; summed={round(p1pc+pcp2,3)}; p1p2={round(p1p2, 3)}')
    if round(p1pc + pcp2,5) == round(p1p2,5):
      passes = True
    
    return passes

  @property
  def maxX(self):
    return max(self._point1.x, self._point2.x)

  @property
  def sameX(self):
    return self._point1.x == self._point2.x

  @property
  def sameY(self):
    return self._point1.y == self._point2.y

  @property
  def maxY(self):
    return max(self._point1.y, self._point2.y)

  def __str__(self):
    return f'Line: {self._point1} to {self._point2}'

#endregion

#region functions



#endregion


# prep variables

lines = []
overallMaxX = 0
overallMaxY = 0

for l in rawLines:
  line = Line(l)
  # if not line.isDiagonal:
  overallMaxX = max(overallMaxX, line.maxX)
  overallMaxY = max(overallMaxY, line.maxY)
  lines.append(line)
  # else:
    # print(f'Diagonal; skipping {line}')

# print(f'\n\n----------------------\n\n')

# for line in lines:
#   print(line)

# print(f'\n\n----------------------\n\n')
print(f'Max X: {overallMaxX}')
print(f'Max Y: {overallMaxY}')

allPoints = [[0 for x in range(overallMaxX+20)] for y in range(overallMaxY+20)]
allIntersectingPoints = 0

index = 0

print(f'About to perform {(overallMaxY+1)*(overallMaxX+1)} calculations...')

for y in range(overallMaxY+1):
  for x in range(overallMaxX+1):
    index += 1
    if index %5000 == 0:
      print(f'performed {index} calculations.')
    for line in lines:
      if line.passesThrough(x, y):
        allPoints[x][y] = allPoints[x][y] + 1
    if allPoints[x][y] > 1:
      allIntersectingPoints += 1

# for y in range(0,overallMaxY+1):
#   res = ''
#   for x in range(0,overallMaxX+1):
#     if allPoints[x][y] == 0:
#       res += ' .'
#     else:
#       res += str(allPoints[x][y]).rjust(2, ' ')
#   print(f'Row {str(y).rjust(3, " ")}: {res}')

print(f'There are {allIntersectingPoints} points where at least two lines overlap')