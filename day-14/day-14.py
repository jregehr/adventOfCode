import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]


# print(lines)
print(f'Loaded {len(lines)} lines.')

memory = [0] * 65535

for line in lines:
  if line[0:4] == 'mask':
    mask = line[7:]
    # print(f'mask={mask}')
  else:
    parts = re.split('\[|\]| ', line)
    # print(f'line={parts}')
    number = str(f'{int(parts[4]):036b}')
    # print(number)

    for pos in range(0, len(mask)):
      if mask[pos] == 'X':
        continue
      else:
        number = number[:pos] + mask[pos] + number[pos+1:]
    # print(number)

    memoryAddress = int(parts[1])
    numberAsBinary = int(number, 2)
    # print(numberAsBinary)
    memory[memoryAddress] = int(number, 2)
    # print('===============================')

sum = 0
for mem in memory:
  sum += mem

print(f'The sum of the memory is {sum}')
