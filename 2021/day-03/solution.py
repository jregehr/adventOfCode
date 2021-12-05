import sys

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

numBits = len(lines[0])

print(f'numBits: {numBits}')

zeroes = [0] * numBits
ones = [0] * numBits

for l in lines:
  # print(f'line: {l}')
  for pos in range(0, numBits):
    if l[pos] == '0':
      zeroes[pos] += 1
    else:
      ones[pos] += 1

print(f'Zeroes: {zeroes}')
print(f'Ones: {ones}')

gamma = ''
epsilon = ''

for pos in range(0, numBits):
  if ones[pos] > zeroes[pos]:
    gamma += '1'
    epsilon += '0'
  else:
    gamma += '0'
    epsilon += '1'

gammaNum =int(gamma, base=2)
epsilonNum = int(epsilon, base=2)


print(f'gamma: {gamma}, or {gammaNum}')
print(f'epsilon: {epsilon}, or {epsilonNum}')
print(f'power consumption = {gammaNum * epsilonNum}')

def keep(array, position, value):
  result = []

  for l in array:
    if l[position] == value:
      result.append(l)
  
  # print(f'keep result: {result}')
  return result

def countZeroesOnes(cArray, position):
  zeroesCount = 0
  onesCount = 0
  for l in cArray:
    if l[position] == '0':
      zeroesCount += 1
    else:
      onesCount += 1
  
  # print(f'countZeroesOnes; pos={position}; zC={zeroesCount}; oC={onesCount}; cArray={cArray}')
  return zeroesCount, onesCount

def mostCommon(mcArray, position):
  zeroesCount, onesCount = countZeroesOnes(mcArray, position)
  if zeroesCount > onesCount:
    print('most common: 0')
    return '0'
  else:
    print('most common: 1')
    return '1'

def leastCommon(lcArray, position):
  zeroesCount, onesCount = countZeroesOnes(lcArray, position)
  if onesCount >= zeroesCount:
    print('least common: 0')
    return '0'
  else:
    print('least common: 1')
    return '1'


print(f'find the o2 genertor rating...')
o2Array = lines
o2ArrayRange = len(o2Array[0])
for pos in range(0, o2ArrayRange):
  o2Array = keep(o2Array, pos, mostCommon(o2Array, pos))
  if len(o2Array) < 2:
    break

o2Num = int(o2Array[0], base=2)
print(f'oxygen generator rating: {o2Array[0]}, or {o2Num}')

print(f'find the co2 scrubber rating...')
co2Array = lines
co2ArrayRange = len(co2Array[0])
for pos in range(0, co2ArrayRange):
  co2Array = keep(co2Array, pos, leastCommon(co2Array, pos))
  if len(co2Array) < 2:
    break

co2Num = int(co2Array[0], base=2)
print(f'CO2 scrubber rating: {co2Array[0]}, or {co2Num}')

print(f'Life support rating = {o2Num * co2Num}')
