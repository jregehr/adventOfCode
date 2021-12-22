import sys
import operator

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
heightmap = []

for l in lines:
  # print(f'line: {l}')
  mapRow = []
  for item in l:
    mapRow.append(int(item))
  heightmap.append(mapRow)

# print(heightmap)

maxX = len(heightmap[0])
maxY = len(heightmap)
notInBasin = 9

def getItem(heightmap, x, y):
  if x < 0 or x >= maxX or y < 0 or y >= maxY:
    return 99
  else:
    return heightmap[y][x]

def addToBasin(heightmap, basinMap, x, y):
  basinMap[f'{x}__{y}'] = heightmap[y][x]

def lessThanSurrounding(heightmap, x, y, value):
  p1 = getItem(heightmap, x - 1, y)
  p2 = getItem(heightmap, x + 1, y)
  p3 = getItem(heightmap, x, y - 1)
  p4 = getItem(heightmap, x, y + 1)

  return value < min(p1, p2, p3, p4)

def checkAddBasin(heightmap, x, y, basinMap, min):
  heightAtLocation = getItem(heightmap, x, y)
  if heightAtLocation > min and heightAtLocation < notInBasin:
    addToBasin(heightmap, basinMap, x, y)
    basin(heightmap, x, y, basinMap, heightAtLocation)

def basin(heightmap, x, y, basinMap, min):
  checkAddBasin(heightmap, x - 1, y, basinMap, min)
  checkAddBasin(heightmap, x + 1, y, basinMap, min)
  checkAddBasin(heightmap, x, y - 1, basinMap, min)
  checkAddBasin(heightmap, x, y + 1, basinMap, min)

lowPointSum = 0
basins = {}
basinSizes = {}

for x in range(maxX):
  for y in range(maxY):
    if lessThanSurrounding(heightmap, x, y, heightmap[y][x]):
      lowPointSum += (heightmap[y][x] + 1)
      basinMap = {}
      addToBasin(heightmap, basinMap, x, y)
      basin(heightmap, x, y, basinMap, heightmap[y][x])
      basins[f'{x}__{y}'] = basinMap
      basinSizes[f'{x}__{y}'] = len(basinMap.values())

print(f'Risk sum = {lowPointSum}')

product = 1

sortedBasinSizes = sorted(basinSizes.values(), reverse=True)

for n in range(3):
  product = product * sortedBasinSizes[n]

print(f'Largest basin product = {product}')