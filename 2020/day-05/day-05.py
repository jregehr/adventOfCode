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

rows = 127
columns = 7

maxSeatId = 0

for seat in lines:

  minRow = 0
  maxRow = rows

  minCol = 0
  maxCol = columns

  for fb in range(0, 7):
    if seat[fb] == 'F':
      maxRow = maxRow - 1 - int((maxRow-minRow)/2)
    elif seat[fb] == 'B':
      minRow = minRow + 1 + int((maxRow-minRow)/2)
    # print(f'seatpos={seat[fb]}, minRow={minRow}, maxRow={maxRow}')

  for lr in range(7, 10):
    if seat[lr] == 'L':
      maxCol = maxCol - 1 - int((maxCol-minCol)/2)
    elif seat[lr] == 'R':
      minCol = minCol + 1 + int((maxCol-minCol)/2)
    # print(f'seatpos={seat[fb]}, minCol={minCol}, maxCol={maxCol}')

  seatId = minRow * 8 + minCol
  # print(f'Seat {seat} is Row {minRow}, Column {minCol}; ID = {seatId}')

  print(seatId)

  maxSeatId = max(maxSeatId, seatId)

print(f'Max SeatId = {maxSeatId}')
