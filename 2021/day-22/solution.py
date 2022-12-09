import sys
import collections

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = [line.strip() for line in f_input]

# print(lines)
print(f'Loaded {len(lines)} lines.')


#region instruction class

class Instruction:
  def __init__(self, rawInstruction):
    # print(f'Instruction: {rawInstruction}')
    state = rawInstruction.split(' ')[0]
    self._state = ON if state == ON else OFF
    self._coordinates = {}

    coordinateInstructions = rawInstruction.split(' ')[1].split(',')
    for coordinateInstruction in coordinateInstructions:
      arrCoordInst = coordinateInstruction.split('=')
      min = int(arrCoordInst[1].split('.')[0])
      max = int(arrCoordInst[1].split('.')[2])
      if min > max:
        floof=min
        min=max
        max=floof
      self._coordinates[f'{arrCoordInst[0]}_min'] = min
      self._coordinates[f'{arrCoordInst[0]}_max'] = max
    
    # print(self)

  @property
  def outsideRange(self):
    result = False

    if max(-50, self._coordinates[X_MIN], self._coordinates[X_MAX]) == -50:
      result = True

    if max(-50, self._coordinates[Y_MIN], self._coordinates[Y_MAX]) == -50:
      result = True

    if max(-50, self._coordinates[Z_MIN], self._coordinates[Z_MAX]) == -50:
      result = True

    if min(50, self._coordinates[X_MIN], self._coordinates[X_MAX]) == 50:
      result = True

    if min(50, self._coordinates[Y_MIN], self._coordinates[Y_MAX]) == 50:
      result = True

    if min(50, self._coordinates[Z_MIN], self._coordinates[Z_MAX]) == 50:
      result = True

    return result

  @property
  def state(self):
    return self._state

  @property
  def minX(self):
    return self._coordinates[X_MIN]

  @property
  def minY(self):
    return self._coordinates[Y_MIN]

  @property
  def minZ(self):
    return self._coordinates[Z_MIN]

  @property
  def maxX(self):
    return self._coordinates[X_MAX]

  @property
  def maxY(self):
    return self._coordinates[Y_MAX]

  @property
  def maxZ(self):
    return self._coordinates[Z_MAX]
  
  def __str__(self):
    return f'{self._state}: x={self._coordinates[X_MIN]} - {self._coordinates[X_MAX]}; y={self._coordinates[Y_MIN]} - {self._coordinates[Y_MAX]}; z={self._coordinates[Z_MIN]} - {self._coordinates[Z_MAX]}'

#endregion

#region constants
ON = 'on'
OFF = 'off'
X_MAX = 'x_max'
Y_MAX = 'y_max'
Z_MAX = 'z_max'
X_MIN = 'x_min'
Y_MIN = 'y_min'
Z_MIN = 'z_min'

RANGE_MIN=-50
RANGE_MAX=50

#endregion

#region functions

def decodeCoordinate(coordinate):
  ## return x_y_z as x, y, z
  coordArray = coordinate.split('_')
  return int(coordArray[0]), int(coordArray[1]), int(coordArray[2])


def encodeCoordnate(x, y, z):
  return f'{x}_{y}_{z}'

def getCubeState(space, coordinate):
  if space.get(coordinate) == None:
    return OFF
  return ON if space[coordinate] == ON else OFF


#endregion


# prep variables
instructions = []
cubes = {}

for l in lines:
  # print(f'line: {l}')
  inst = Instruction(l)
  # if not inst.outsideRange:
  instructions.append(inst)

for i in instructions:
  print(f'Running {i}')
  for x in range(i.minX, i.maxX+1):
    for y in range(i.minY, i.maxY+1):
      for z in range(i.minZ, i.maxZ+1):
        cubes[encodeCoordnate(x, y, z)] = i.state


print('Counting ...')
onCount = sum(1 for v in cubes.values() if v == ON)

print(f'{onCount} cubes are on.')