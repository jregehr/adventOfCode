import re
import sys
import csv

if len(sys.argv) != 3:
  sys.exit('Please pass the file name and the containing bag color as arguments.')

file = sys.argv[1]
bagColor = sys.argv[2]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]


# print(lines)
print(f'Loaded {len(lines)} lines.')

bagRelationships = {}
# contained bag is the key
# containing bags array is the value


def getBagColor(bag):
  sbag = bag.split(' ')
  return f'{sbag[1]} {sbag[2]}'


for bagLine in lines:
  relship = bagLine.split(' bags contain ')
  if relship[1] == 'no other bags.':
    continue

  containedBags = relship[1].split(', ')
  for containedBag in containedBags:
    cBagCol = getBagColor(containedBag)
    containedBagFitsIn = bagRelationships.get(cBagCol)
    if containedBagFitsIn == None:
      bagRelationships[cBagCol] = [relship[0]]
    else:
      bagRelationships[cBagCol].append(relship[0])

# for bagRel in bagRelationships.keys():
#   print(f'{bagRel} goes in {bagRelationships[bagRel]}')

containables = set()


def canContain(bagColor, containables):
  # print(f'entering canContain({bagColor})')
  containers = bagRelationships.get(bagColor)
  if containers == None:
    print('outermost')
    # return f'\n{bagColor}'
    containables.add(bagColor)
    return containables

  for containerColor in containers:
    containables.add(containerColor)
    # retVal += f'\n{containerColor}'
    # retVal += f'{canContain(containerColor)} contains {bagColor} '
    containables = canContain(containerColor, containables)
  return containables


containables = canContain(bagColor, containables)
print(len(containables))
print(containables)
# canContain(bagColor)
