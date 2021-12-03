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
  # print(f'\n=== {x} ====================================\n{lines[x]}')
  if lines[x] == '':
    continue
  lines[x] = dict(x.split(":") for x in re.split('\n| ', lines[x].strip()))

# for line in lines:
#   print(line)

print(f'Loaded {len(lines)} lines.')


# fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
required_fields = [
    ['byr', 'Birth Year', 1920, 2002],
    ['iyr', 'Issue Year', 2010, 2020],
    ['eyr', 'Expiration Year', 2020, 2030],
    ['ecl', 'Eye Color', ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']],
    ['hcl', 'Hair Color', '#', 'hex'],
    ['pid', 'Passport ID', 9],
    ['hgt', 'Height', ['cm', 150, 193], ['in', 59, 76]]
]

validCount = 0
invalidCount = 0

for passport in lines:

  print(f'DEBUG: testing {passport}')
  validPassport = True

  for required_field in required_fields:
    fieldName = required_field[0]
    # print(f'looking for {fieldName} in {passport}')
    field = passport.get(fieldName)
    if field is None:
      invalidCount += 1
      validPassport = False
      break

    if fieldName in ['byr', 'iyr', 'eyr']:
      fnum = int(field)
      if fnum < required_field[2] or fnum > required_field[3]:
        invalidCount += 1
        validPassport = False
        break

    if required_field[0] == 'ecl':
      if field not in required_field[2]:
        invalidCount += 1
        validPassport = False
        break

    if required_field[0] == 'hcl':
      if field[0] != '#' or not re.match('[0-9a-z]{6}$', field[1:]):
        invalidCount += 1
        validPassport = False
        break

    if required_field[0] == 'pid':
      if not re.match('[0-9]{9}$', field):
        invalidCount += 1
        validPassport = False
        break

    if required_field[0] == 'hgt':
      if len(field) < 4:
        invalidCount += 1
        validPassport = False
        break

      height = int(field[:-2])
      if field[-2:] == 'cm':
        if height < required_field[2][1] or height > required_field[2][2]:
          invalidCount += 1
          validPassport = False
      elif field[-2:] == 'in':
        if height < required_field[3][1] or height > required_field[3][2]:
          invalidCount += 1
          validPassport = False
      else:
        invalidCount += 1
        validPassport = False

  if validPassport:
    validCount += 1

print(f'I found {validCount} valid passports and {invalidCount} invalid passports.')
