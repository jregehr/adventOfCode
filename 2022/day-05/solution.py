import sys
import queue

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

#region SMALL
# q1 = queue.LifoQueue()
# q1.put("Z")
# q1.put("N")

# q2 = queue.LifoQueue()
# q2.put("M")
# q2.put("C")
# q2.put("D")

# q3 = queue.LifoQueue()
# q3.put("P")
#endregion

# region INPUT

q1 = queue.LifoQueue()
q1.put("B")
q1.put("L")
q1.put("D")
q1.put("T")
q1.put("W")
q1.put("C")
q1.put("F")
q1.put("M")

q2 = queue.LifoQueue()
q2.put("N")
q2.put("B")
q2.put("L")

q3 = queue.LifoQueue()
q3.put("J")
q3.put("C")
q3.put("H")
q3.put("T")
q3.put("L")
q3.put("V")

q4 = queue.LifoQueue()
q4.put("S")
q4.put("P")
q4.put("J")
q4.put("W")

q5 = queue.LifoQueue()
q5.put("Z")
q5.put("S")
q5.put("C")
q5.put("F")
q5.put("T")
q5.put("L")
q5.put("R")

q6 = queue.LifoQueue()
q6.put("W")
q6.put("D")
q6.put("G")
q6.put("B")
q6.put("H")
q6.put("N")
q6.put("Z")

q7 = queue.LifoQueue()
q7.put("F")
q7.put("M")
q7.put("S")
q7.put("P")
q7.put("V")
q7.put("G")
q7.put("C")
q7.put("N")

q8 = queue.LifoQueue()
q8.put("W")
q8.put("Q")
q8.put("R")
q8.put("J")
q8.put("F")
q8.put("V")
q8.put("C")
q8.put("Z")

q9 = queue.LifoQueue()
q9.put("R")
q9.put("P")
q9.put("M")
q9.put("L")
q9.put("H")
# endregion


### SMALL
# queues = [ 0, q1, q2, q3] 
### INPUT
queues = [ 0, q1, q2, q3, q4, q5, q6, q7, q8, q9] 
ending = ""

##### Part I
# for l in lines:
#   print('=================================')
#   print(f'line: {l}')
#   actions = l.split(' ')
#   # count = int(actions[1])
#   for i in range(int(actions[1])):
#     x = queues[int(actions[3])].get()
#     print(f'popped {x}')
#     queues[int(actions[5])].put(x)
#   # print(queues)

##### Part II
for l in lines:
  print('=================================')
  print(f'line: {l}')
  actions = l.split(' ')
  # count = int(actions[1])
  x = queue.LifoQueue()
  for i in range(int(actions[1])):
    x.put(queues[int(actions[3])].get())

  # print(f'after: {x.queue}')
  # for s in x.queue:
  while not x.empty():
    s = x.get()
    queues[int(actions[5])].put(s)

ending += queues[1].get()
ending += queues[2].get()
ending += queues[3].get()
ending += queues[4].get()
ending += queues[5].get()
ending += queues[6].get()
ending += queues[7].get()
ending += queues[8].get()
ending += queues[9].get()

print(f'tops: {ending}')