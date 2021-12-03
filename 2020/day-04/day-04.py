import re
import sys
import csv
import copy
import math

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file, 'r') as f:
  contents = f.read()

lines = re.split('\n{2}', contents)
for x in range(0, len(lines)):
  lines[x] = re.split('\n| ', lines[x])

# for line in lines:
#   print(line)

print(f'Loaded {len(lines)} lines.')

# fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

validCount = 0
invalidCount = 0

for passport in lines:
  hasfields = "|"
  validPassport = True
  for field in passport:
    hasfields += field.split(':')[0]

  for field in required_fields:
    if hasfields.count(field) == 0:
      invalidCount += 1
      validPassport = False
      break

  if validPassport:
    validCount += 1

print(f'I found {validCount} valid passports and {invalidCount} invalid passports.')
