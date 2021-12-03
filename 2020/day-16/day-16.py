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

fields = []
myticket = []
nearbyTickets = []
validTickets = []


def ticketValuesAsNumArray(ticketlist):
  ret = []
  for sVal in ticketlist.split(','):
    ret.append(int(sVal))

  return ret


def isValidField(fieldValue):
  field = list(filter(lambda field: (field[1] <= fieldValue and field[2] >= fieldValue), fields))
  # print(f'Debug: fieldValue[{fieldValue}] found {field}')
  return field is not None and len(field) > 0


def possibleFields(fieldValue):
  return list(filter(lambda field: (field[1] <= fieldValue and field[2] >= fieldValue), fields))


index = 0
fieldCount = 0
# fields
while True:
  if lines[index] == '':
    index += 1
    break

  fieldLineStuff = lines[index].split(': ')
  fieldName = fieldLineStuff[0]
  fieldCount += 1
  values = fieldLineStuff[1].split(' or ')
  for value in values:
    hilo = value.split('-')
    fields.append([fieldName, int(hilo[0]), int(hilo[1])])

  index += 1

# my ticket
index += 1
myticket = ticketValuesAsNumArray(lines[index])

index += 3
for ticket in range(index, len(lines)):
  nearbyTickets.append(ticketValuesAsNumArray(lines[ticket]))

# print(f'fields:')
# print(fields)
# print('======================')
# print(f'my ticket: {myticket}')
# print('======================')
# print('near by tickets:')
# print(nearbyTickets)
# sys.exit()


# validate tickets
invalidSum = 0
for nearbyTicket in nearbyTickets:
  validTicket = True
  for field in nearbyTicket:
    # if isValidField(field):
    if len(possibleFields(field)) > 0:
      continue
    else:
      invalidSum += field
      validTicket = False
      break

  if validTicket:
    validTickets.append(nearbyTicket)

print(f'Scanning error rate: {invalidSum}')

print(f'There are {len(validTickets)} valid and {len(nearbyTickets)} total tickets.')

fieldPositions = [[] for x in range(fieldCount)]

for validTicket in validTickets:
  for x in range(fieldCount):
    lpossibleFields = possibleFields(validTicket[x])
    possibleFieldNames = []
    for possibleField in lpossibleFields:
      possibleFieldNames.append(possibleField[0])
    if fieldPositions[x] == None or len(fieldPositions[x]) == 0:
      fieldPositions[x] = set(possibleFieldNames)
    else:
      fieldPositions[x] = set(possibleFieldNames).intersection(fieldPositions[x])

# for fieldPosition in fieldPositions:
#   print(fieldPosition)

iterations = 0
# print(f'=====================================')
while iterations < 30:
  iterations += 1
  for singleFPs in list(filter(lambda fp: (len(fp) == 1), fieldPositions)):
    sfpVal = list(singleFPs)[0]
    for fp in fieldPositions:
      if len(fp) > 1 and sfpVal in fp:
        # print(f'singleFP:{sfpVal}; fp:{fp}')
        fp.remove(list(singleFPs)[0])

  # print(f'=== iteration {iterations} ===================')
  # for fieldPosition in fieldPositions:
  #   print(fieldPosition)
  if len(list(filter(lambda fp: (len(fp) > 1), fieldPositions))) == 0:
    print(f'found all fields in {iterations} iterations.')
    break

iter = 0
for fieldPosition in fieldPositions:
  print(f'{iter}: {fieldPosition}')
  iter += 1

print(myticket)
