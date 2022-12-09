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

def makeCubeFor(instruction, indexes):
  print(f'making cube for {instruction}')
  for x in range(instruction.minX, instruction.maxX+1):
    for y in range(instruction.minY, instruction.maxY+1):
      for z in range(instruction.minZ, instruction.maxZ+1):
        if indexes[0] %500 == 0:
        # print(f'At index {index}: x={x}, y={y}, z={z}')
          print(f'At index {indexes[0]}: x={x}, y={y}, z={z}')
        indexes[0] += 1

        yield encodeCoordnate(x, y, z)

#endregion

# prep variables
instructions = []
cubes = set()

for l in lines:
  # print(f'line: {l}')
  inst = Instruction(l)
  if not inst.outsideRange:
    instructions.append(inst)

indexes=[0]

for i in instructions:
  cubeForI = makeCubeFor(i, indexes)
  if i.state == ON:
    cubes = cubes.union(cubeForI)
  else:
    cubes = cubes.difference(cubeForI)
print(f'At end index {indexes[0]}')




print(f'{len(cubes)} cubes are on.')