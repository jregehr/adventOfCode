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

containedBagRelationships = {}
# contained bag is the key
# containing bags array is the value

containingBagRelationships = {}
# containing bag is the key
# contained bags array is the value


def getBagColor(bag):
    sbag = bag.split(' ')
    return f'{sbag[1]} {sbag[2]}'


def getNumberAndBagColor(bag):
    sbag = bag.split(' ')
    return [int(sbag[0]), f'{sbag[1]} {sbag[2]}']


for bagLine in lines:
    relship = bagLine.split(' bags contain ')
    if relship[1] == 'no other bags.':
        continue

    containedBags = relship[1].split(', ')
    for containedBag in containedBags:
        cBagCol = getBagColor(containedBag)
        containedBagFitsIn = containedBagRelationships.get(cBagCol)
        if containedBagFitsIn == None:
            containedBagRelationships[cBagCol] = [relship[0]]
        else:
            containedBagRelationships[cBagCol].append(relship[0])
        cNumBagCol = getNumberAndBagColor(containedBag)
        bagContainedBy = containingBagRelationships.get(relship[0])
        if bagContainedBy == None:
            containingBagRelationships[relship[0]] = [cNumBagCol]
        else:
            containingBagRelationships[relship[0]].append(cNumBagCol)

print('=== contained bag relationships ==============')
for bagRel in containedBagRelationships.keys():
    print(f'{bagRel} goes in {containedBagRelationships[bagRel]}')

print('=== containing bag relationships ==============')
for bagRel in containingBagRelationships.keys():
    print(f'{bagRel} has {containingBagRelationships[bagRel]}')

containables = set()
bagCount = 0


def canContain(bagColor, containables):
  # print(f'entering canContain({bagColor})')
  containers = containedBagRelationships.get(bagColor)
  if containers == None:
      # print('outermost')
      # return f'\n{bagColor}'
      containables.add(bagColor)
      return containables

  for containerColor in containers:
      containables.add(containerColor)
      # retVal += f'\n{containerColor}'
      # retVal += f'{canContain(containerColor)} contains {bagColor} '
      containables = canContain(containerColor, containables)
  return containables


def bagContains(bagColor, bagCount):
  print(f'entering bagContains({bagColor})')
  containers = containingBagRelationships.get(bagColor)
  if containers == None:
    print(f'{bagColor} is empty')
    return bagCount

  for container in containers:
    print(f'contains {container[0]} {container[1]}')
    # bagCount += 1                                  #the bag we are in
    bagCountA = container[0]                       # the bags we contain
    bagCountB = bagContains(container[1], 1)
    bagCount += (bagCountA * bagCountB)
    # bagCount = bagContains(container[1], bagCount) # the bags they contain
    
  return bagCount


print('\n\n=== results =========================')


containables = canContain(bagColor, containables)
print(f'{len(containables)} bags can contain a {bagColor} bag.')
print(containables)

bagCount = bagContains(bagColor, bagCount)
print(f'A {bagColor} bag contains {bagCount} bags')
