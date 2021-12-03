import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')


# Read in the file
with open(file) as f:
  starters = f.read().strip().split(',')

print(starters)
print(f'Loaded {len(starters)} lines.')

tracker = {}

count = 1
lastNum = None
lastLast = None
for num in starters:
  spoken = int(num)
  print(f'Turn {count}; Speak: {spoken}')
  tracker[spoken] = [count]
  lastNum = spoken
  count += 1

while count <= 30000000:  # 2020:
  lastSpoken = tracker.get(lastNum)

  if lastSpoken == None or len(lastSpoken) == 1:
    spoken = 0
  else:
    spoken = lastSpoken[0] - lastSpoken[1]
  # print(f'Turn {count}; Speak: {spoken}; lastSpoken: {lastSpoken}')
  if tracker.get(spoken) == None:
    tracker[spoken] = [count]
  else:
    tracker[spoken].insert(0, count)
    if len(tracker[spoken]) > 10:
      tracker[spoken] = tracker[spoken][:3]
  lastNum = spoken

  count += 1

  if count % 100000 == 0:
    print(f'At count {count}')

print(f'Last Number Spoken: {lastNum}')
