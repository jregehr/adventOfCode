import re
import sys
import csv
import math

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

print(lines)
print(f'Loaded {len(lines)} lines.')


#region Debug Printers

def debug_print(phase, output):
  if debug <= phase:
    print(output)


LINE_BREAK = '================================================'


def debug_line_break(phase):
  debug_print(phase, LINE_BREAK)

#endregion


##############################################
debug = 1
##############################################

player1 = []
player2 = []

deck = player1
for x in range(1, len(lines)):
  if lines[x] == "":
    deck = player2
    continue

  if lines[x].startswith('Player'):
    continue

  deck.append(int(lines[x]))

debug_print(1, player1)
debug_print(1, player2)

round = 0

while len(player1) > 0 and len(player2) > 0:
  round += 1
  roundWinner = ''
  print(f'-- Round {round} --')
  print(f'Player 1\'s deck: {player1}')
  print(f'Player 2\'s deck: {player2}')
  p1Card = player1.pop(0)
  p2Card = player2.pop(0)
  print(f'Player 1 plays: {p1Card}')
  print(f'Player 2 plays: {p2Card}')
  if p1Card > p2Card:
    roundWinner = 'player1'
    player1.append(p1Card)
    player1.append(p2Card)
  else:
    roundWinner = 'player2'
    player2.append(p2Card)
    player2.append(p1Card)
  print(f'{roundWinner} wins the round!\n')

winnerDeck = None
if len(player1) > 0:
  print(f'\n\nGame won by player1')
  winnerDeck = player1
else:
  print(f'\n\nGame won by player2')
  winnerDeck = player2

print('== Post-game results ==')
print(f'Player 1\'s deck: {player1}')
print(f'Player 2\'s deck: {player2}')

mult = 1
finalScore = 0
for card in range(len(winnerDeck)-1, -1, -1):
  finalScore += winnerDeck[card] * mult
  mult += 1

print(f'Final Score: {finalScore}')