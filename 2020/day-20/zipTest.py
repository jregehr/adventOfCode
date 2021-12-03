
original = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

new = list(zip(*original[::-1]))

print('== original =============================')
for row in original:
  print(row)

print('== new ==================================')
for row in new:
  print(list(row))
