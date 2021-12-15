import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

def addFishAtDay(fishes, day, addFishCount):
  fishCount = fishes.get(day)
  if fishCount == None:
    fishes[day] = addFishCount
  else:
    fishes[day] = fishCount + addFishCount


def countFish(fishes):
  count = 0

  for day in fishes.keys():
    count += fishes.get(day)

  return count

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = f_input.readlines()

# print(lines)
print(f'Loaded {len(lines)} lines.')

# prep variables

fishes = {}

# setup the hash
for day in lines[0].split(','):
  print(f'day={day}')
  iDay = int(day)
  addFishAtDay(fishes, iDay, 1)

print(f'{fishes}')




days = 18
days = 80
days = 256
for day in range(days):
  todayFish = {}
  for day in fishes.keys():
    if day == 0:
      # these fish will reproduce
      addFishAtDay(todayFish, 8, fishes.get(0))
      addFishAtDay(todayFish, 6, fishes.get(0))
    else:
      addFishAtDay(todayFish, (day-1), fishes.get(day))
  fishes = todayFish

print(f'After {days} days, there are {countFish(fishes)} fish.')