import re
import sys
import csv
import copy
import math

if len(sys.argv) != 4:
  sys.exit('Please pass the file name as an argument, plus a start and duration (0 = forever)')

file = sys.argv[1]
start = int(sys.argv[2])
duration = int(sys.argv[3])

print(f'Loading {file}')

# Read in the file
with open(file, 'r') as f:
  contents = f.read()

lines = re.split('\n', contents)

theTime = start  # int(lines[0])

busses = lines[1].split(',')

for line in lines:
  print(line)
print(f'Loaded {len(lines)} lines.')

theCount = 0
theStep = 1  # int(busses[0])

for x in range(0, len(busses)):
  if busses[x] == 'x':
    busses[x] = -1
  else:
    abus = int(busses[x])
    busses[x] = abus

# print(busses)
theTime = 15258950540
theStep = 4774818883  # 924556795459165  # 421097
theStep = 924556795459165  # 421097

while duration == 0 or theCount < duration:
  # if theTime % theStep != 0:
  #   print(f'theTime is {theTime}, stepping 1')
  #   theTime += 1
  #   continue

  theCount += 1
  theTime += theStep
  outputs = []

  if theTime % 50000 == 0:
    print(f'Time is {theTime}, {theCount} iterations')

  leTime = theTime
  for bus in range(0, len(busses)):
    # print(f'bus {bus}: {busses[bus]}')
    if busses[bus] == -1:
      # outputs.append(f'{leTime}: Bus {bus}, {busses[bus]}, is skipped')
      pass
    else:
      # busNum = int(busses[bus])

      # if leTime < busses[bus]:
      #   # print('time is too low')
      #   break

      if leTime % busses[bus] == 0:
        # outputs.append(f'{leTime}: Bus {bus}, {busses[bus]} leaves now')
        # print(f'{leTime}: Bus {bus}, {busses[bus]} leaves now')
        pass
      else:
        # print(f'{leTime}: bus does not leave now')
        # outputs.append(f'{leTime}: Bus {bus}, {busses[bus]} DOES NOT leave now')
        break

    leTime += 1
    # The bus left at the right time

    if bus == len(busses) - 1:
      print(f'We did it. At time {theTime} the busses all leave when they are supposed to!')
      for output in outputs:
        print(output)
      sys.exit()

  # # if theTime % 50 == 0:
  # print('=== DEBUG ======================')
  # for output in outputs:
  #   print(output)
