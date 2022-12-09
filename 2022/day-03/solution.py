import sys
import collections

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

priority = {
  "a": 1,
  "b": 2,
  "c": 3,
  "d": 4,
  "e": 5,
  "f": 6,
  "g": 7,
  "h": 8,
  "i": 9,
  "j": 10,
  "k": 11,
  "l": 12,
  "m": 13,
  "n": 14,
  "o": 15,
  "p": 16,
  "q": 17,
  "r": 18,
  "s": 19,
  "t": 20,
  "u": 21,
  "v": 22,
  "w": 23,
  "x": 24,
  "y": 25,
  "z": 26,
  "A": 27,
  "B": 28,
  "C": 29,
  "D": 30,
  "E": 31,
  "F": 32,
  "G": 33,
  "H": 34,
  "I": 35,
  "J": 36,
  "K": 37,
  "L": 38,
  "M": 39,
  "N": 40,
  "O": 41,
  "P": 42,
  "Q": 43,
  "R": 44,
  "S": 45,
  "T": 46,
  "U": 47,
  "V": 48,
  "W": 49,
  "X": 50,
  "Y": 51,
  "Z": 52
}

priorityTotal = 0

for l in lines:
  print(f'line: {l}')
  llen = len(l)
  hllen = int(llen/2)
  # print(f'llen:{llen};hllen:{hllen}')
  stra = l[0:hllen]
  strb = l[hllen:llen]
  # print(f'a:{stra}')
  # print(f'b:{strb}')
  ssa = set(list(stra))
  ssb = set(list(strb))
  common = list(ssa.intersection(ssb))[0]
  priorityTotal += priority[common]
  print(f'Common:{common}, with pri {priority[common]}')

print('==============================')
print(f'Priority total: {priorityTotal}')


count = 0
packs = ["", "", ""]
total = 0
for l in lines:
  print(f'line: {l}')
  count += 1
  packs[count%3] = l
  if count % 3 == 0:
    ssa = set(list(packs[0]))
    ssb = set(list(packs[1]))
    ssc = set(list(packs[2]))

    common = list(ssa.intersection(ssb).intersection(ssc))[0]
    total += priority[common]

print('===============================================')
print(f'total priority for three-elf sets: {total}')

