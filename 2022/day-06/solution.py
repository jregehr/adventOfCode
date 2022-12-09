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

for l in lines:
  # print(f'line: {l}')
  print('=======================================')
  print(f'String {l[0:20]}')
  s = l
  for c in range(13,len(s)):
    # print(f'{c}:{s[c-3]}{s[c-2]}{s[c-1]}{s[c]}')
    # print(f'real {c}: {s[c-3:c+1]}; set: {set(list(s[c-3:c+1]))}')
    sset = set(list(s[c-13:c+1]))
    # print(f'set len : {len(s)}')
    if len(sset) == 14:
      print(f'at {c+1}: {s[c-3:c+1]}')
      break

