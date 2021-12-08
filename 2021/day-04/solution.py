import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = f_input.readlines()

# print(lines)
print(f'Loaded {len(lines)} lines.')

#region BingoCard

class BingoCard:

  CARD_SIZE = 5
  MATCH = 'X'

  def __init__(self):
    self._card = [[None for c in range(BingoCard.CARD_SIZE)] for r in range(BingoCard.CARD_SIZE)]
    self._matches  = [[' ' for c in range(BingoCard.CARD_SIZE)] for r in range(BingoCard.CARD_SIZE)]
    self._winner = False
    self._wins = 0
    self._firstWinUnmarkedSum = 0
    self._firstCalledWin = -1

  @property
  def winner(self):
    return self._winner
  
  @property
  def firstWinUnmarkedSum(self):
    return self._firstWinUnmarkedSum

  @property
  def firstCalledWin(self):
    return self._firstCalledWin
  
  @property
  def firstWinFinalScore(self):
    return self._firstCalledWin * self._firstWinUnmarkedSum

  def callNumber(self, calledNumber):
    for r in range(0, BingoCard.CARD_SIZE):
      for c in range(0, BingoCard.CARD_SIZE):
        if self._card[r][c] == calledNumber:
          self._matches[r][c] = BingoCard.MATCH
          self.checkForBingo(r, c)
          if self._winner and self._wins == 1 and self._firstCalledWin == -1:
            self._firstCalledWin = calledNumber
          break
  
  def setRow(self, rowNum, rowData):
    arrRowData = rowData.split()
    for col in range(0, BingoCard.CARD_SIZE):
      self._card[rowNum][col] = int(arrRowData[col].strip())

  def checkForBingo(self, row, column):
    rowBingo = True
    for loopColumn in range(0, BingoCard.CARD_SIZE):
      if self._matches[row][loopColumn] != BingoCard.MATCH:
        rowBingo = False
        break
    
    colBingo = True
    for loopRow in range(0, BingoCard.CARD_SIZE):
      if self._matches[loopRow][column] != BingoCard.MATCH:
        colBingo = False
        break
    
    if rowBingo or colBingo:
      self._winner = True
      self._wins += 1
      if self._wins == 1 and self._firstWinUnmarkedSum == 0:
        self._firstWinUnmarkedSum = self.sumUnmarked()
        print('First WIN!')


  def sumUnmarked(self):
    result = 0
    for r in range(0, BingoCard.CARD_SIZE):
      for c in range(0, BingoCard.CARD_SIZE):
        if self._matches[r][c] != BingoCard.MATCH:
          result += self._card[r][c]
    
    return result

  def __str__(self):
    result = 'This card is '
    if  not self._winner:
      result += 'NOT '
    result += f'a winner and has {self._wins} wins.\n'
    if self._wins == 1:
      result += f'+++++ first win final score: {self.firstWinFinalScore}\n'
    for r in range(0, BingoCard.CARD_SIZE):
      for c in range(0, BingoCard.CARD_SIZE):
        result += str(self._card[r][c]).rjust(3, ' ') + self._matches[r][c]
      result += '\n'
    return result

# endregion

# prep variables

calledNumbers = lines[0].split(',')

cards = []

cardStart = 2

while cardStart < len(lines):
  thisCard = BingoCard()
  for cardLine in range(0, BingoCard.CARD_SIZE):
    # print(f'cardstart={cardStart}; cardLine={cardLine}; line={lines[cardStart+cardLine]}')
    thisCard.setRow(cardLine, lines[cardStart+cardLine])

  cards.append(thisCard)
  cardStart += (1 + BingoCard.CARD_SIZE)

print(f'Loaded {len(cards)} bingo cards.')

haveAWinner = False

for calledNum in calledNumbers:
  # if haveAWinner:
  #   break
  for card in cards:
    nCalledNum = int(calledNum)
    card.callNumber(nCalledNum)
    if card.winner:
      unMarkedSum = card.sumUnmarked()
      if unMarkedSum == 0:
        print(f'no unmarked numbers left.')
      else:
        print(f'After calling {calledNum}...\n{card}')
        print(f'Unmarked sum is {unMarkedSum}; First win unmarked sum is {card.firstWinUnmarkedSum} final score is {nCalledNum * unMarkedSum}.')
      # haveAWinner = True
      # break