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


def nested(rulenumber, nested_rule):

  if nested_rule.count(rulenumber) > 1:
    debug_line_break(99)
    debug_line_break(99)
    debug_print(99, f'Rule {rulenumber} is too nested and I just cannot even! See: {nested_rule}')
    debug_line_break(99)
    debug_line_break(99)
    sys.exit()

  fixed = False

  rule = nested_rule
  if rule.strip().endswith(rulenumber):
    # Rule like 8: 42 | 42 8
    rule = rule.replace(rulenumber, '')
    if '|' in rule:
      ruleSplit = [bit.strip() for bit in rule.split('|')]
      ruleSplit = [x.strip() for x in rule.split('|')]
      if ruleSplit[0] == ruleSplit[1]:
        # rule = f'(( {ruleSplit[0]} )|( {ruleSplit[0]}  {ruleSplit[0]} ))'
        rule = f'(( 42 )+)'
        # rule = f'(( 42 )+)'
        fixed = True
    else:
      rule = f'(( {rule} )+)'
      fixed = True

  else:
    # Rule is like 11: 42 31 | 42 11 31
    parts = [x.strip() for x in rule.split('|')]
    parts[0] = [x.strip() for x in parts[0].split(' ')]
    parts[1] = [x.strip() for x in parts[1].split(' ')]
    debug_print(0, f'0: {parts[0]}; 1: {parts[1]}')

    if parts[0][0] == parts[1][0] and parts[0][len(parts[0])-1] == parts[1][len(parts[1])-1]:
      # rule = f'(( {parts[0][0]} )( {parts[0][0]} )?( {parts[0][len(parts[0])-1]} )+)'
      # rule = f'((( {parts[0][0]} )( {parts[0][0]} )?( {parts[0][len(parts[0])-1]} )) | (( {parts[0][0]} )( {parts[0][len(parts[0])-1]} )+) )'
      # rule = f'( ( {parts[0][0]} {parts[0][len(parts[0])-1]} )|( {parts[0][0]} {parts[0][0]} {parts[0][len(parts[0])-1]} )|( {parts[0][0]} ( {parts[0][len(parts[0])-1]} +))     )'
      rule = '(( 42 )( 31 )+)'
      fixed = True

  if fixed:
    debug_line_break(99)
    debug_print(99, f'Rule {rulenumber}: |{nested_rule}| becomes |{rule}')
    debug_line_break(99)
  else:
    debug_line_break(99)
    debug_line_break(99)
    debug_print(99, f'Rule {rulenumber} is not something I understand! See: {rule}')
    debug_line_break(99)
    debug_line_break(99)
    sys.exit()

  return rule


debug = 0

##########################################################################################
# Attempt #2
##########################################################################################

index = 0
rawRules = {}
finishedRules = {}
messages = []

# Load the raw rules
while index < len(lines):
  line = lines[index]
  # debug_print(0, line)
  if line == "":
    index += 1
    break

  lineSplit = line.split(':')
  rule_id = lineSplit[0]
  rule = f'{lineSplit[1]} '.replace(' ', '  ')
  if f' {rule_id} ' in rule:
    rule = nested(rule_id, rule)
  if '|' in rule:
    rule = f'(( {rule} ))'.replace('|', ')|(')
  rawRules[rule_id] = rule
  index += 1

# sys.exit()

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
  debug_print(1, f'Pass {compileCount}; {len(rawRules)} raw, {len(finishedRules)} finished.')
  # debug_print(0, f'Pass {compileCount}: {finishedRules}')
  # debug_print(0, f'Pass {compileCount}: {rawRules}')
  for f in sorted(finishedRules.keys()):
    debug_print(0, f'finishedRule {f}: {finishedRules[f]}')
  for r in sorted(rawRules.keys()):
    debug_print(0, f'rawRule {r}: {rawRules[r]}')

  finishCount = len(finishedRules)

  for fKey in list(finishedRules.keys()):

    hasIts = [key for key, val in rawRules.items() if fKey in val]
    for hasIt in hasIts:
      rawRule = rawRules[hasIt]
      rawRule = rawRule.replace(f' {fKey} ', f' {finishedRules[fKey]} ')
      # rawRule = rawRule.replace(f' {fKey} ', f' {finishedRules[fKey]} ')

      if re.search('[0-9]', rawRule) is None:
        # This one is fully matched. Move it to finished.
        finishedRules[hasIt] = rawRule
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
  if isMatch is not None:
    matches += 1
    print(f'{m} matches the rule:\n{isMatch.group(0)}\n')
  else:
    print(f'{m} does not match the rule.')


print(f'{matches} messages match the rule.')
