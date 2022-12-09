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

containers=0
anyOverlaps=0

for l in lines:
  # print(f'line: {l}')
  first=l.split(',')[0]
  second=l.split(',')[1]
  firsta=int(first.split('-')[0])
  firstb=int(first.split('-')[1])
  seconda=int(second.split('-')[0])
  secondb=int(second.split('-')[1])

  if (firsta <= seconda and firstb >= secondb) or (seconda <= firsta and secondb >= firstb):
    containers +=1
    print(f'fully contained: {l}')

  if seconda <= firsta <= secondb or \
     seconda <= firstb <= secondb or \
     firsta <= seconda <= firstb or \
     firsta <= secondb <= firstb:
    anyOverlaps += 1
    print(f'overlap: {l}')

print(f'there are {containers} full-containers.')
print(f'there are {anyOverlaps} overlappers.')