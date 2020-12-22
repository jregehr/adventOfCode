import re
import sys
import csv
import math
import copy

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

# print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

# print(lines)
# print(f'Loaded {len(lines)} lines.')


#region Debug Printers

def debug_print(phase, output):
  if debug <= phase:
    print(output)


LINE_BREAK = '================================================'


def debug_line_break(phase):
  debug_print(phase, LINE_BREAK)

#endregion


##############################################
debug = 2
##############################################

#region Data Loading

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

#endregion

#region game play

def play(player1, player2, gameNum=1):

  playedDecks = {}
  if gameNum == 1:
    games = 1
  else:
    games = gameNum
  print(f'=== Game {gameNum} ===')
  round = 0

  while len(player1) > 0 and len(player2) > 0:
    alreadyPlayed = playedDecks.get(f'{str(player1)}|{str(player2)}')
    if alreadyPlayed is not None:
      print('This round has been played already. Award the win to Player 1')
      return 'Player 1'

    playedDecks[f'{str(player1)}|{str(player2)}'] = True

    round += 1
    roundWinner = ''
    print(f'\n-- Round {round} (Game {gameNum}) --')
    print(f'Player 1\'s deck: ', end='')
    print(*player1, sep=', ')
    print(f'Player 2\'s deck: ', end='')
    print(*player2, sep=', ')
    print(f'==== g{gameNum}r{round}: |', end='')
    print(*player1, sep=', ', end='')
    print('|', end='')
    print(*player2, sep=', ', end='')
    print('|')
    p1Card = player1.pop(0)
    p2Card = player2.pop(0)
    print(f'Player 1 plays: {p1Card}')
    print(f'Player 2 plays: {p2Card}')
    if len(player1) >= p1Card and len(player2) >= p2Card:
      #sub-game!!
      subDeck1 = copy.deepcopy(player1[0:p1Card])
      subDeck2 = copy.deepcopy(player2[0:p2Card])
      games += 1
      print('Playing a sub-game to determine the winner...\n')
      roundWinner = play(subDeck1, subDeck2, games)
      print(f'\n...anyway, back to game {gameNum}.')
    else:
      if p1Card > p2Card:
        roundWinner = 'Player 1'
      else:
        roundWinner = 'Player 2'

    if roundWinner == 'Player 1':
      player1.append(p1Card)
      player1.append(p2Card)
    else:
      player2.append(p2Card)
      player2.append(p1Card)
    print(f'{roundWinner} wins round {round} of game {gameNum}!')

  winnerDeck = None
  if len(player1) > 0:
    print(f'The winner of game {gameNum} is player 1!')

    if gameNum > 1:
      return 'Player 1'
    winnerDeck = player1
  else:
    print(f'The winner of game {gameNum} is player 2!')
    if gameNum > 1:
      return 'Player 2'
    winnerDeck = player2

  if gameNum == 1:
    print('== Post-game results ==')
    print(f'Player 1\'s deck: ', end='')
    print(*player1, sep=', ')
    print(f'Player 2\'s deck: ', end='')
    print(*player2, sep=', ')

    mult = 1
    finalScore = 0
    for card in range(len(winnerDeck)-1, -1, -1):
      finalScore += winnerDeck[card] * mult
      mult += 1

    print(f'Final Score: {finalScore}')

#endregion

play(player1, player2)