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

memory = {}
count = 0


for line in lines:
  count += 1
  if count % 10 == 0:
    print(f'processed {count} lines')

  if line[0:4] == 'mask':
    mask = line[7:]
    # print(f'mask={mask}')
  else:
    parts = re.split(r'\[|\]| ', line)
    # print(f'line={parts}')
    numberToWrite = int(parts[4])
    # print(numberToWrite)

    address = str(f'{int(parts[1]):036b}')

    for pos in range(0, len(mask)):
      if mask[pos] == '0':
        continue
      else:
        address = address[:pos] + mask[pos] + address[pos+1:]
    # print(address)

    placeholders = address.count('X')
    addresses = [address] * (2 ** placeholders)

    for x in range(0, len(addresses)):
      minimask = str(f'{x:0{placeholders}b}')
      # print(minimask)
      for y in range(0, len(minimask)):
        addresses[x] = addresses[x].replace('X', minimask[y], 1)

      # memory[int(addresses[x], 2)] = numberToWrite
      memory[addresses[x]] = numberToWrite

    addresss = []

sum = 0
for mem in memory.values():
  sum += mem

print(f'The sum of the memory is {sum}')
