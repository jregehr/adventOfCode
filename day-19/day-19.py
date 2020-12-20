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


def debug_print(phase, output):
  if debug <= phase:
    print(output)


LINE_BREAK = '================================================'


def debug_line_break(phase):
  debug_print(phase, LINE_BREAK)


rawRules = {}
finishedRules = {}
messages = []

debug = 0
index = 0

# Load the raw rules
while index < len(lines):
  line = lines[index]
  debug_print(0, line)
  if line == "":
    index += 1
    break

  lineSplit = line.split(':')
  rawRules[lineSplit[0]] = lineSplit[1]
  index += 1

# The rest are messages
messages = lines[index:]

debug_line_break(0)
debug_print(1, 'Raw Rules to start:')
for r in rawRules.keys():
  debug_print(0, f'{r}: {rawRules[r]}')
debug_line_break(0)

AB_ONLY = re.compile(r'^[ab ]+$')

theOneRule = re.compile(r'^a(((aa|bb)(ab|ba))|((ab|ba)(aa|bb)))b$')

compileCount = 0
finishCount = 0
while finishedRules.get('0') is None:
  compileCount += 1

  # special first-run processing: remove quotes from the initial letter rules
  if compileCount == 1:
    letters = [key for key, val in rawRules.items() if re.search(r'[a-z]', val) is not None]
    for letter in letters:
      finishedRules[letter] = rawRules[letter].replace('"', '').strip()
      rawRules.pop(letter)
    debug_print(1, f'First pass: {finishedRules}')
    continue

  debug_line_break(0)
  debug_print(0, f'Pass {compileCount}: {finishedRules}')
  debug_print(0, f'Pass {compileCount}: {rawRules}')
  debug_print(1, f'Pass {compileCount}; {len(rawRules)} raw, {len(finishedRules)} finished.')

  finishCount = len(finishedRules)

  for fKey in list(finishedRules.keys()):

    hasIts = [key for key, val in rawRules.items() if fKey in val]
    for hasIt in hasIts:
      rawRule = rawRules[hasIt] + ' '
      if not 'X' in rawRule:
        rawRule = rawRule.replace('|', 'X')

      rawRule = rawRule.replace(f' {fKey} ', f' {finishedRules[fKey]} ')
      if re.search('[0-9]', rawRule) is None:
        # This one is fully matched. Bracket and pipe it.
        if 'X' in rawRule and '|' in rawRule:
          finishedRules[hasIt] = f'(({rawRule.replace("X", ") | (")}))'
        elif 'X' in rawRule:
          finishedRules[hasIt] = f'({rawRule.replace("X", " | ")})'
        else:
          # finishedRules[hasIt] = rawRule
          finishedRules[hasIt] = f'{rawRule}'
        # elif AB_ONLY.match(rawRule):
        #   finishedRules[hasIt] = rawRule.replace(' ', '')
        # else:
        rawRules.pop(hasIt)
      else:
        rawRules[hasIt] = rawRule

  if finishCount == len(finishedRules) and compileCount > 3:
    debug_line_break(1)
    debug_print(1, 'the finish count has not changed.')
    debug_line_break(1)
    debug_print(1, 'Finished Rules:')
    for key in sorted(finishedRules.keys()):
      debug_print(1, f'{key}: {finishedRules[key]}')
    debug_line_break(1)
    debug_print(1, 'Raw Rules:')
    for key in sorted(rawRules.keys()):
      debug_print(1, f'{key}: {rawRules[key]}')
    debug_line_break(1)
    sys.exit()


debug_print(99, f'Looped {compileCount} times to produce {finishedRules["0"]}')
debug_print(99, f'There are {len(finishedRules)} finished rules and {len(rawRules)} left over.')

ruleWillBe = '^' + finishedRules['0'].replace(' ', '') + '$'
debug_print(99, ruleWillBe)
theOneRule = re.compile(ruleWillBe)

# debug_print(0, '================================================')
# debug_print(0, rawRules)

# debug_print(0, '================================================')
# debug_print(0, messages)

matches = 0
for m in messages:
  isMatch = theOneRule.match(m)
  if isMatch == None:
    print(f'{m} does not match the rule.')
  else:
    matches += 1
    print(f'{m} matches the rule: {isMatch.group(0)}')

print(f'{matches} messages match the rule.')
