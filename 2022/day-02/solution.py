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
opponent = { "A": "Rock", "B": "Paper", "C": "Scissors" }
player =       { "X": "Rock", "Y": "Paper", "Z": "Scissors" }
playerpoints = { "X": 1,      "Y": 2,       "Z": 3 }
roundpoints = {
  "AX": 3, # Rock     v Rock
  "BY": 3, # Paper    v Paper 
  "CZ": 3, # Scissors v Scissors
  "AY": 6, # Rock     v Paper 
  "AZ": 0, # Rock     v Scissors
  "BX": 0, # Paper    v Rock
  "BZ": 6, # Paper    v Scissors
  "CX": 6, # Scissors v Rock
  "CY": 0, # Scissors v Paper 
}

totalPoints = 0

for l in lines:
  # print(f'line: {l}')
  round = l.split(' ')
  print(f'Opp:{round[0]}:{opponent[round[0]]}, Me:{round[1]}:{player[round[1]]}; Points = {playerpoints[round[1]]} + {roundpoints[round[0]+round[1]]}')
  totalPoints += playerpoints[round[1]] + roundpoints[round[0]+round[1]]

print(f'Total points: {totalPoints}')

## part 2

desiredOutcomes = {
  "X": "Lose",
  "Y": "Draw",
  "Z": "Win!"
}

playForOutComes = {
  "A X": "Scissors",
  "A Y": "Rock",
  "A Z": "Paper",
  "B X": "Rock",
  "B Y": "Paper",
  "B Z": "Scissors",
  "C X": "Paper",
  "C Y": "Scissors",
  "C Z": "Rock",
}

outcomes = { 
  "A X": 3,   #o:rock,     m:scissors LOSE = 3
  "A Y": 4,   #o:rock,     m:rock     DRAW = 4
  "A Z": 8,   #o:rock,     m:paper    WIN! = 8
  "B X": 1,   #o:paper,    m:rock     LOSE = 1
  "B Y": 5,   #o:paper,    m:paper    DRAW = 5
  "B Z": 9,   #o:paper,    m:scissors WIN! = 9
  "C X": 2,   #o:scissors, m:paper    LOSE = 2
  "C Y": 6,   #o:scissors, m:scissors DRAW = 6
  "C Z": 7    #o:scissors, m:rock     WIN! = 7
}

realTotalPoints = 0

print('=================================')

for l in lines:
  round = l.split(' ')
  # print(f'l:{l}')
  print(f'Opp:{round[0]}:{opponent[round[0]]}, MeMust:{round[1]}:{desiredOutcomes[round[1]]}:{playForOutComes[l]}; Points = {outcomes[l]}')
  realTotalPoints += outcomes[l]

print(f'Real Total points: {realTotalPoints}')

