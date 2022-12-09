import sys
import math

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = [line.strip() for line in f_input]


# print(lines)
print(f'Loaded {len(lines)} lines.')

# prep variables

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

  @property
  def position(self):
    return str(self._x)+","+str(self._y)
  
  def move(self, direction, amount):
    if direction == "L":
      self._x -= amount
    
    if direction == "R":
      self._x += amount
    
    if direction == "U":
      self._y -= amount
    
    if direction == "D":
      self._y += amount
  
  def catchUp(self, point2):
    dist = self.length(point2)
    if dist < 2:
      return
    
    if dist == 2:
      if self._x == point2.x:
        # move Y
        if self._y < point2.y:
          self._y += 1
        else:
          self._y -= 1
      else:
        # move X
        if self._x < point2.x:
          self._x += 1
        else:
          self._x -= 1
      return
    
    # move diagonally
    if self._y < point2.y:
      self._y += 1
    else:
      self._y -= 1
    if self._x < point2.x:
      self._x += 1
    else:
      self._x -= 1

  def length(self, point2):
    return math.sqrt((self._x - point2.x)**2 + (self._y - point2.y)**2)
  
  def __str__(self):
    return f'Point: {self._x},{self._y}'

#endregion

H = Point("4,-1")
T = Point("3,0")
print(f'dist: {H.length(T)}')
H = Point("0,0")
H1 = Point("0,0")
H2 = Point("0,0")
H3 = Point("0,0")
H4 = Point("0,0")
H5 = Point("0,0")
H6 = Point("0,0")
H7 = Point("0,0")
H8 = Point("0,0")
T = Point("0,0")
positions = set()

for l in lines:
  print(f'line: {l}')
  instruction = l.split(' ')
  direction = instruction[0]
  amount = int(instruction[1])
  for m in range(0,amount):
    H.move(direction, 1)
    H1.catchUp(H)
    H2.catchUp(H1)
    H3.catchUp(H2)
    H4.catchUp(H3)
    H5.catchUp(H4)
    H6.catchUp(H5)
    H7.catchUp(H6)
    H8.catchUp(H7)
    T.catchUp(H8)
    positions.add(T.position)
    print(f'1:{H} | 1:{H1} | 2:{H2} | 3:{H3} | 4:{H4} | 5:{H5} | 6:{H6} | 7:{H7} | 8:{H8} | T:{T} | dist: {H.length(T)}')

x = list(positions)
x.sort()
print(x)
print(f'All positions = {len(positions)}')