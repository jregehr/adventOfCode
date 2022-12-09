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


def isVisible(treeArray, x, y):
  if x == 0 or y == 0 or x == len(treeArray[0])-1 or y == len(treeArray)-1:
    # print(f'tree {x},{y} is visible')
    return 1
  
  height = treeArray[y][x]

  #left side
  visLeft = 1
  for xn in range(0,x):
    if treeArray[y][xn] >= height:
      visLeft = 0
      break

  #right side
  visRight = 1
  for xn in range(x+1,len(treeArray[0])):
    if treeArray[y][xn] >= height:
      visRight = 0
      break

  #above
  visAbove = 1
  for yn in range(0, y):
    if (treeArray[yn][x]) >= height:
      visAbove = 0
      break

  #below
  visBelow = 1
  for yn in range(y+1, len(treeArray)):
    if (treeArray[yn][x]) >= height:
      visBelow = 0
      break

  if visLeft + visRight + visAbove + visBelow == 0:
    # print(f'tree {x},{y} is not visible')
    return 0
  # print(f'tree {x},{y} is visible')
  return 1

def scenicScore(treeArray, x, y):
 
  height = treeArray[y][x]

  #left side
  scoreLeft = 0
  for xn in range(x-1,-1,-1):
    scoreLeft += 1
    if treeArray[y][xn] >= height:
      break

  #right side
  scoreRight = 0
  for xn in range(x+1,len(treeArray[0])):
    scoreRight += 1
    if treeArray[y][xn] >= height:
      break

  #above
  scoreAbove = 0
  for yn in range(y-1, -1, -1):
    scoreAbove += 1
    if (treeArray[yn][x]) >= height:
      break

  #below
  scoreBelow = 0
  for yn in range(y+1, len(treeArray)):
    scoreBelow += 1
    if (treeArray[yn][x]) >= height:
      break
  
  result = scoreLeft * scoreRight * scoreAbove * scoreBelow
  # print(f'XY {x},{y}; H:{height} A:{scoreAbove} B:{scoreBelow} L:{scoreLeft} R:{scoreRight}; {result}')
  return result
  
forestLines = []

width = 0
length = 0

for l in lines:
  # print(f'line: {l}')
  forestLines.append(l)
  length += 1

width = len(forestLines[0])

visibles = 0
highestScenicScore = 0


for x in range(0, width):
  # print('')
  for y in range(0, length):
    visibles += isVisible(forestLines, x, y)
    highestScenicScore = max(highestScenicScore, scenicScore(forestLines, x, y))

print(f'{visibles} trees are visible.')
print(f'Highest scenic score: {highestScenicScore}')