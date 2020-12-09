import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = list(f_input.read().split())

# print(lines)
print(f'Loaded {len(lines)} lines.')

solution = False

## Loop the file on itself, checking for the 2020 sum
for l1 in lines:
  if solution:
    break

  for l2 in lines:
    num1 = int(l1)
    num2 = int(l2)
    if num1 + num2 == 2020:
      solution = True
      print(f'{l1} and {l2} sum to 2020. Their product is {num1 * num2}')
      break

## Triple-loop the file on itself, checking for the 2020 sum
solution = False

for l1 in lines:
  if solution:
    break

  for l2 in lines:
    if solution:
      break

    for l3 in lines:
      num1 = int(l1)
      num2 = int(l2)
      num3 = int(l3)
      if num1 + num2 + num3 == 2020:
        solution = True
        print(
            f'{l1}, {l2}, and {l3} sum to 2020. Their product is {num1 * num2 * num3}')
        break

## Print the sum and the product.
