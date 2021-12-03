import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = f_input.readlines()

# print(lines)
print(f'Loaded {len(lines)} lines.')

# prep variables

for l in lines:
  print(f'line: {l}')