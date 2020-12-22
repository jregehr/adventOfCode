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

# print(lines)
print(f'Loaded {len(lines)} lines.')


#region Debug Printers

def debug_print(phase, output):
  if debug <= phase:
    print(output)


LINE_BREAK = '================================================'


def debug_line_break(phase):
  debug_print(phase, LINE_BREAK)

#endregion

#region Functions


# def rotate(tile):
#   ## Do the work
#   new_lines = [[0]*10]*10
#   lines = tile[LINES]
#   for x in range(9, -1, -1):
#     for y in range(0, 10):
#       new_lines[x][y] =

#   debug_line_break(3)
#   debug_print(3, f'Lines as they were:')
#   for line in tile[LINES]:
#     debug_print(3, line)
#   debug_line_break(3)
#   debug_print(3, f'Lines as they are now, rotated:')
#   for line in new_lines:
#     debug_print(3, line)
#   debug_line_break(3)

#   tile[LINES] = new_lines


def reverse(tile):

  debug_line_break(2)
  debug_print(2, f'Lines as they were:')
  for line in tile[LINES]:
    debug_print(2, line)

  ## Do the work
  for x in range(len(tile[LINES])):
    tile[LINES][x] = tile[LINES][x][::-1]

  debug_line_break(2)
  debug_print(2, f'Lines as they are now, reversed:')
  for line in tile[LINES]:
    debug_print(2, line)
  debug_line_break(2)


def flip(tile):
  new_lines = list(reversed(tile[LINES]))

  debug_line_break(1)
  debug_print(1, f'Lines as they were:')
  for line in tile[LINES]:
    debug_print(1, line)
  debug_line_break(1)
  debug_print(1, f'Lines as they are now, flipped:')
  for line in new_lines:
    debug_print(1, line)
  debug_line_break(1)

  tile[LINES] = new_lines

class Tile:
  def __init__(self, id, rows):
    self._id = id
    self._rows = rows
    self._matches = [None]*4
    self._edges = [None]*4
    self._match_sides = [None]*4
    self._matched_sides = [False]*4
    self._placed = False

  @property
  def rows(self):
    return self._rows

  @property
  def matches(self):
    return self._matches

  @property
  def edges(self):
    return self._edges

  @property
  def match_sides(self):
    return self._match_sides

  @property
  def matched_sides(self):
    return self._matched_sides

  @property
  def placed(self):
    return self._placed






def print_tile(tile, debug_level=99):
  debug_print(debug_level, f'--- tile {tile[ID]} -------------------------------------')
  for line in tile[LINES]:
    debug_print(debug_level, line)
  debug_print(debug_level, f'---------------------------------------------------')
  debug_print(debug_level, f'Edges: {tile[EDGES]}')
  debug_print(debug_level, f'Matches: {tile[MATCHES]}')
  debug_print(debug_level, f'Match sides: {tile[MATCH_SIDES]}')
  debug_print(debug_level, f'Matched sides: {tile[MATCHED_SIDES]}')
  debug_print(debug_level, f'Placed: {tile[PLACED]}')
  debug_print(debug_level, f'---------------------------------------------------')


def find_edges(tile):
  tile[EDGES][EDGE_TOP] = tile[LINES][0]
  tile[EDGES][EDGE_BOTTOM] = tile[LINES][9]
  left = ''
  right = ''
  for x in tile[LINES]:
    # left should be bottom to top
    left = x[0] + left
    # right should be top to bottom
    right += x[-1]
  tile[EDGES][EDGE_LEFT] = left
  tile[EDGES][EDGE_RIGHT] = right


def check_match(tile0, tile1):
  if tile0[ID] == tile1[ID]:
    return

  for x in range(0, 4):
    for y in range(0, 4):
      if tile0[EDGES][x] == tile1[EDGES][y] or tile0[EDGES][x][::-1] == tile1[EDGES][y]:
        tile0[MATCHES][x] = tile1[ID]
        tile0[MATCH_SIDES][x] = y
        tile1[MATCHES][y] = tile0[ID]
        tile1[MATCH_SIDES][y] = x
        return


def find_edge_match(edge, tile):
  debug_print(4, f'Edge: {edge}, Tile {tile[ID]} Edges: {tile[EDGES]}')
  for x in range(0, 4):
    if tile[EDGES][x] is not None and (edge == tile[EDGES][x] or edge[::-1] == tile[EDGES][x]):
      tile[MATCHED_SIDES][x] = True
      return x

  return None


def find_match(edge, tiles):
  for tile in tiles:
    # if tile[PLACED]:
    #   continue
    found_edge = find_edge_match(edge, tile)
    if found_edge is not None:
      return tile, found_edge

  return None, None


def update_matched_edge(edge, tile):
  for x in range(0, 4):
    if tile[EDGES][x] is not None and (edge == tile[EDGES][x] or edge[::-1] == tile[EDGES][x]):
      tile[MATCHED_SIDES][x] = True


def opposite_edge(edgeNumber):
  if edgeNumber > 1:
    return edgeNumber - 2
  return edgeNumber + 2


def find_tiles(tiles, matches):
  found_tiles = []
  for tile in tiles:
    if len(list(filter(None, tile[MATCHES]))) == matches:
      found_tiles.append(tile)

  return found_tiles


def first_unmatched_edge(tile):
  if tile[MATCHES][EDGE_LEFT] is not None and not tile[MATCHED_SIDES][EDGE_LEFT]:
    return tile[EDGES][EDGE_LEFT]
  if tile[MATCHES][EDGE_TOP] is not None and not tile[MATCHED_SIDES][EDGE_TOP]:
    return tile[EDGES][EDGE_TOP]
  if tile[MATCHES][EDGE_RIGHT] is not None and not tile[MATCHED_SIDES][EDGE_RIGHT]:
    return tile[EDGES][EDGE_RIGHT]
  return tile[EDGES][EDGE_BOTTOM]


def check_unmatched_edge(tile, edgeNumber):
  if not tile[MATCHED_SIDES][edgeNumber]:
    return tile[EDGES][edgeNumber]

  return None

#endregion

#region Constants


ID = 'tileId'
LINES = 'lines'
TILE_LINE = 'Tile '
EDGES = 'edges'
MATCHES = 'matches'
MATCH_SIDES = 'match-sides'
MATCHED_SIDES = 'matched-sides'
PLACED = 'placed'
EDGE_LEFT = 0
EDGE_TOP = 1
EDGE_RIGHT = 2
EDGE_BOTTOM = 3

CORNER_MATCHES = 2
EDGE_MATCHES = 3
MIDDLE_MATCHES = 4

#endregion

##################################################################
##################################################################
debug = 6
##################################################################
##################################################################

#region Data loading

tiles = []
tile = {}

tileId = ""
for x in range(len(lines)):
  line = lines[x]
  if line.startswith(TILE_LINE):
    tile = {}
    tileId = line[5:9]
    debug_print(0, f'tileId: {tileId}')
    tile[ID] = tileId
    tile[LINES] = []
    tile[MATCHES] = [None]*4
    tile[EDGES] = [None]*4
    tile[MATCH_SIDES] = [None]*4
    tile[MATCHED_SIDES] = [False]*4
    tile[PLACED] = False
    tiles.append(tile)
    continue

  if line == '':
    continue

  tile[LINES].append(line)
# append the last tile

for tile in tiles:
  find_edges(tile)

print(f'There are {len(tiles)} tiles.')

grid_size = int(math.sqrt(len(tiles)))

solution = [[-1 for i in range(int(grid_size))] for j in range(int(grid_size))]

debug_print(99, f'solution grid: {solution}')

#endregion

for tile0 in tiles:
  for tile1 in tiles:
    check_match(tile0, tile1)

# for tile in tiles:
#   print_tile(tile, 4)

corners = find_tiles(tiles, CORNER_MATCHES)
edges = find_tiles(tiles, EDGE_MATCHES)
middles = find_tiles(tiles, MIDDLE_MATCHES)

debug_line_break(5)
debug_print(5, 'Corners:')
for tile in corners:
  print_tile(tile, 5)

# debug_line_break(3)
# debug_print(3, 'Edges:')
# for tile in edges:
#   print_tile(tile, 3)

solution[0][0] = corners[0]
corners[0][PLACED] = True

# debug_line_break(99)
# debug_print(99, 'Top Corner')
# print_tile(corners[0])

# find the middle of the top row
edge_to_match = first_unmatched_edge(solution[0][0])
for x in range(1, grid_size-1):
  debug_print(5, f'Top Row, tile {x}')
  tile, edge = find_match(edge_to_match, edges)
  if tile is not None:
    solution[0][x] = tile
    tile[PLACED] = True
    edge_to_match = check_unmatched_edge(tile, opposite_edge(edge))
    if edge_to_match is None:
      debug_print(99, 'Something bwoke - first row edge matching')
      sys.exit()
  else:
    debug_print(4, 'Something bwoke')

# edge_to_match = first_unmatched_edge(solution[0][grid_size-2])
solution[0][grid_size-1], edge = find_match(edge_to_match, corners)
update_matched_edge(edge_to_match, solution[0][grid_size-2])

debug_line_break(6)
debug_print(6, 'Solution:')
for y in range(0, 3):
  for x in range(0, 3):
    tile = solution[y][x]
    if tile == 0:
      tile = 'None'
    elif isinstance(tile, dict):
      tile = f'Tile {tile[ID]}'
    debug_print(6, f'SOLN {x},{y}: {tile}')


# following rows
for y in range(1, grid_size):
  for x in range(grid_size):
    upper_edge_match = first_unmatched_edge(solution[y-1][x])
    look_in = middles
    if y+1 == grid_size and (x == 0 or x+1 == grid_size):
      look_in = corners
    elif y+1 == grid_size or (x == 0 or x+1 == grid_size):
      look_in = edges
    tile, edge = find_match(upper_edge_match, look_in)
    if tile:
      solution[y][x] = tile
      tile[PLACED] = True
      update_matched_edge(upper_edge_match, solution[y-1][x])

    # left_upper_edge_match = first_unmatched_edge(solution[x-1][0])
    # tile, edge = find_match(left_upper_edge_match, edges)
    # solution[x][0] = tile
    # right_upper_edge_match = first_unmatched_edge(solution[x-1][grid_size-1])
    # tile, edge = find_match(right_upper_edge_match, edges)
    # solution[x][grid_size-1] = tile


debug_line_break(99)
debug_print(99, 'FINAL Solution:')
for y in range(0, 3):
  for x in range(0, 3):
    tile = solution[y][x]
    if tile == 0:
      tile = 'None'
    elif isinstance(tile, dict):
      tile = f'Tile {tile[ID]}'
    print(f'SOLN {x},{y}: {tile}')
