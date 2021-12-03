import re
import sys
import csv
import math
import copy

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

# print(lines)
print(f'Loaded {len(lines)} lines.')


# region Debug Printers

def debug_print(phase, output):
  if debug <= phase:
    print(output)


LINE_BREAK = '================================================'


def debug_line_break(phase):
  debug_print(phase, LINE_BREAK)

# endregion

# region Tile class


class Tile:

  TILE_LINE = 'Tile '
  EDGE_LEFT = 0
  EDGE_TOP = 1
  EDGE_RIGHT = 2
  EDGE_BOTTOM = 3

  CORNER_MATCHES = 2
  EDGE_MATCHES = 3
  MIDDLE_MATCHES = 4

  PLACEMENT_LEFT = 0
  PLACEMENT_TOP = 1
  PLACEMENT_RIGHT = 2
  PLACEMENT_BOTTOM = 3
  PLACEMENT_MIDDLE = 4
  PLACEMENT_BOTTOM_LEFT = 5

  PRINT_TYPE_FULL = 'full'
  PRINT_TYPE_ID = 'id'

  print_type = PRINT_TYPE_FULL

  def __init__(self, id):
    self._id = id
    self._rows = []
    self._matches = [None]*4
    self._edges = [None]*4
    self._match_sides = [None]*4
    self._matched_sides = [False]*4
    self._placed = False

  @property
  def id(self):
    return self._id

  @property
  def rows(self):
    return self._rows

  @rows.setter
  def rows(self, value):
    self._rows = value
    if len(self._rows) == 10:
      self.__find_edges()

  def add_row(self, row):
    self._rows.append(row)
    if len(self._rows) == 10:
      self.__find_edges()

  @property
  def matches(self):
    return self._matches

  @matches.setter
  def matches(self, value):
    self._matches = value

  @property
  def edges(self):
    return self._edges

  @edges.setter
  def edges(self, value):
    self._edges = value

  @property
  def match_sides(self):
    return self._match_sides

  @match_sides.setter
  def match_sides(self, value):
    self._match_sides = value

  @property
  def matched_sides(self):
    return self._matched_sides

  @matched_sides.setter
  def matched_sides(self, value):
    self._matched_sides = value

  @property
  def placed(self):
    return self._placed

  @placed.setter
  def placed(self, value):
    self._placed = value

  def print(self, debug_level=99):
    debug_print(debug_level, f'--- tile {self._id} -------------------------------------')
    for line in self._rows:
      debug_print(debug_level, line)
    debug_print(debug_level, f'---------------------------------------------------')
    debug_print(debug_level, f'Edges: {self._edges}')
    debug_print(debug_level, f'Matches: {self._matches}')
    debug_print(debug_level, f'Match sides: {self._match_sides}')
    debug_print(debug_level, f'Matched sides: {self._matched_sides}')
    debug_print(debug_level, f'Placed: {self._placed}')
    debug_print(debug_level, f'---------------------------------------------------')


  ### Print_* are used to print a tile and its surroudings. Combined output:
    # |       T234       |
    # | L234 -ME23- R234 |
    # |       B234       |
  def print_top(self):
    return f' |       {self._matches[Tile.EDGE_TOP]}       | '

  def print_middle(self):
    return f' | {self._matches[Tile.EDGE_LEFT]} -{self._id}- {self._matches[Tile.EDGE_RIGHT]} | '
  
  def print_bottom(self):
    return f' |       {self._matches[Tile.EDGE_BOTTOM]}       | '

  def borderless(self):
    result = []
    for row in range(1, len(self._rows)-1):
      result.append(self._rows[row][1:9])
    return result

  def __repr__(self):
    if Tile.print_type == Tile.PRINT_TYPE_FULL:
      return f'{self._id}: Placed({self._placed}), Edges {self._edges}'
    elif Tile.print_type == Tile.PRINT_TYPE_ID:
      return f'{self._id}'

  def __str__(self):
    return f'Tile {self._id}: Placed({self._placed}), Matches: {self._matches}, Edges {self._edges}'

  def __find_edges(self):
    self._edges[Tile.EDGE_TOP] = self._rows[0]
    self._edges[Tile.EDGE_BOTTOM] = self._rows[9][::-1]
    left = ''
    right = ''
    for x in self._rows:
      # left should be bottom to top
      left = x[0] + left
      # right should be top to bottom
      right += x[-1]
    self._edges[Tile.EDGE_LEFT] = left
    self._edges[Tile.EDGE_RIGHT] = right

  def check_match(self, tile1):
    if self._id == tile1.id:
      # don't match myself.
      return

    for x in range(0, 4):
      for y in range(0, 4):
        if self._edges[x] == tile1.edges[y] or self._edges[x][::-1] == tile1.edges[y]:
          self._matches[x] = tile1.id
          self._matched_sides[x] = y
          tile1.matches[y] = self._id
          tile1.match_sides[y] = x
          return

  def adjust_to_match(self, matching_tile_ids, matching_edge, matching_side, placement):
    # matching_tile_id - the ID of the tile to adjust to
    # matching_edge    - the edge pixles of the tile to adjust to
    # matching_side    - the side that needs to match the tile to adjust to
    print(f'ID: {self._id}, MTIDs: {matching_tile_ids}, mEdge: {matching_edge}, mSide: {matching_side}, plc: {placement}')
    if matching_tile_ids[0] == self._matches[matching_side]:
      # already rotated the right way
      print('already matching the matching side')
      if placement == Tile.PLACEMENT_TOP and self._matches[Tile.EDGE_BOTTOM] is None:
        self.flip()
        return

    if placement == Tile.PLACEMENT_TOP:
      print('top might need a flip')
      while matching_tile_ids[0] != self._matches[matching_side]:
        self.rotate()
      if self._matches[Tile.EDGE_BOTTOM] is None:
        self.flip()
      return

    if placement == Tile.PLACEMENT_LEFT:
      print('left')
      while self._matches[Tile.EDGE_LEFT] is not None:
        self.rotate()
      if self._matches[Tile.EDGE_TOP] != matching_tile_ids[0]:
        self.flip()
      return

    if placement == Tile.PLACEMENT_RIGHT:
      print('right')
      while self._matches[Tile.EDGE_RIGHT] is not None:
        self.rotate()
      return

    if placement == Tile.PLACEMENT_BOTTOM_LEFT:
      print('bottom left')
      while self._matches[Tile.EDGE_TOP] is None or self._matches[Tile.EDGE_RIGHT] is None:
        self.rotate()
      if matching_tile_ids[0] != self._matches[Tile.EDGE_TOP]:
        self.rotate()
        self.flip()
      return

    # middle or bottom
    print('middlebottom')
    while matching_tile_ids[0] != self._matches[matching_side]:
      print('rot and hi mom')
      self.rotate()
    if matching_tile_ids[1] != self._matches[Tile.EDGE_TOP]:
      print('flip')
      self.flip()
    print('done')
    return


  def rotate(self):
    # debug_print(99, 'rotate')
    debug_line_break(3)
    debug_print(3, f'Lines as they were:')
    for row in self._rows:
      debug_print(3, row)

    new_rows = list(zip(*self._rows[::-1]))
    for x in range(len(new_rows)):
      new_rows[x] = ''.join(new_rows[x])

    self._rows = new_rows
    self._edges = self.__rotate_edge_part(self._edges)
    self._matches = self.__rotate_edge_part(self._matches)
    self._match_sides = self.__rotate_edge_part(self._match_sides)
    self._matched_sides = self.__rotate_edge_part(self._matched_sides)

    debug_line_break(3)
    debug_print(3, f'Lines as they are now, rotated:')
    for row in self._rows:
      debug_print(3, row)
    debug_line_break(3)
  
  def __rotate_edge_part(self, edge_part):
    return [ edge_part[3], edge_part[0], edge_part[1], edge_part[2] ]

  # def reverse(self):
  #   debug_print(99, 'reverse')
  #   debug_line_break(6)
  #   debug_print(6, f'REVERSE: Lines as they were:')
  #   for row in self._rows:
  #     debug_print(6, row)

  #   # Do the work
  #   for x in range(len(self._rows)):
  #     self._rows[x] = self._rows[x][::-1]

  #   self.__reverse_edges()
  #   self._matches = self.__reverse_edge_part(self._matches)
  #   self._match_sides = self.__reverse_edge_part(self._match_sides)
  #   self._matched_sides = self.__reverse_edge_part(self._matched_sides)

  #   debug_line_break(6)
  #   debug_print(6, f'Lines as they are now, reversed:')
  #   for row in self._rows:
  #     debug_print(6, row)
  #   debug_line_break(6)

  # def __reverse_edge_part(self, edge_part):
  #   return [ edge_part[2], edge_part[1], edge_part[0], edge_part[3] ]

  # def __reverse_edges(self):
  #   self._edges = [ self._edges[2], self._edges[1][::-1], self._edges[0], self._edges[3][::-1] ]
  #   # self._edges = [ self._edges[2], self._edges[1], self._edges[0], self._edges[3] ]


  def flip(self):
    # debug_print(99, 'flip')
    new_rows = list(reversed(self._rows))

    self._edges = self.__flip_edge_part(self._edges)
    self._matches = self.__flip_edge_part(self._matches)
    self._match_sides = self.__flip_edge_part(self._match_sides)
    self._matched_sides = self.__flip_edge_part(self._matched_sides)

    debug_line_break(5)
    debug_print(5, f'FLIP: Lines as they were:')
    for row in self._rows:
      debug_print(5, row)
    debug_line_break(5)
    debug_print(5, f'Lines as they are now, flipped:')
    for row in new_rows:
      debug_print(5, row)
    debug_line_break(5)

    self._rows = new_rows

  def __flip_edge_part(self, edge_part):
    return [ edge_part[0], edge_part[3], edge_part[2], edge_part[1] ]

# endregion

# region Functions


def opposite_edge(edgeNumber):
  if edgeNumber > 1:
    return edgeNumber - 2
  return edgeNumber + 2


def find_tiles_of_type(tiles, matches):
  found_tiles = []
  for tile in tiles:
    if len(list(filter(None, tile.matches))) == matches:
      found_tiles.append(tile)

  return found_tiles

def searching_for_corner(grid_size, x, y):
  if y == 0 or y+1 == grid_size:
    if x == 0 or x+1 == grid_size:
      return True

  return False

def searching_for_edge(grid_size, x, y):
  if searching_for_corner(grid_size, x, y):
    return False

  return y == 0 or y+1 == grid_size or x == 0 or x+1 == grid_size

def calc_placement(grid_size, x, y):
  if y == 0:
    return Tile.PLACEMENT_TOP
  if x == 0 and y+1 == grid_size:
    return Tile.PLACEMENT_BOTTOM_LEFT
  if x == 0:
    return Tile.PLACEMENT_LEFT
  if y+1 == grid_size:
    return Tile.PLACEMENT_BOTTOM
  if x+1 == grid_size:
    return Tile.PLACEMENT_RIGHT
  return Tile.PLACEMENT_MIDDLE

def print_solution(solution):
  Tile.print_type = Tile.PRINT_TYPE_ID
  print('Solution grid:')
  for y in range(len(solution)):
    cnum = '[   ' 
    top = '[   '
    middle = f'[ {y} '
    bottom = '[   '
    for x in range(len(solution[y])):
      m = (' None ' if solution[y][x] == -1 else solution[y][x].print_middle())
      cnum += ' |' + ' ' * int(len(m)/2-3) + f'{x}' + ' ' * int(len(m)/2-2) + '| '
      top    += ('      ' if solution[y][x] == -1 else solution[y][x].print_top())
      middle += m
      bottom += ('      ' if solution[y][x] == -1 else solution[y][x].print_bottom())
    print(f'{cnum} ]')
    print(f'{top} ]')
    print(f'{middle} ]')
    print(f'{bottom} ]')
    print()
  Tile.print_type = Tile.PRINT_TYPE_FULL


# endregion

##################################################################
##################################################################
debug = 7
##################################################################
##################################################################

# region Data loading

tiles = []

tileId = ""
for x in range(len(lines)):
  line = lines[x]
  if line.startswith(Tile.TILE_LINE):
    tileId = line[5:9]
    debug_print(0, f'tileId: {tileId}')
    tile = Tile(tileId)
    tiles.append(tile)
    continue

  if line == '':
    continue

  tile.add_row(line)

print(f'There are {len(tiles)} tiles.')

grid_size = int(math.sqrt(len(tiles)))

solution = [[-1 for i in range(int(grid_size))] for j in range(int(grid_size))]

# debug_print(99, f'solution grid: {solution}')
print_solution(solution)

for tile in tiles:
  tile.print(1)


# endregion

for tile0 in tiles:
  for tile1 in tiles:
    tile0.check_match(tile1)

corners = find_tiles_of_type(tiles, Tile.CORNER_MATCHES)
edges = find_tiles_of_type(tiles, Tile.EDGE_MATCHES)
middles = find_tiles_of_type(tiles, Tile.MIDDLE_MATCHES)

debug_line_break(4)
debug_print(4, "All Tiles")
if debug <= 4:
  for tile in tiles:
    print(tile)


debug_line_break(4)
debug_print(4, "Corner Tiles")
if debug <= 4:
  for tile in corners:
    # tile.print()
    print(tile)

# set up top corner tile
topCorner = corners[0]
print(f'starter  {topCorner}')
# if topCorner.matches[Tile.EDGE_BOTTOM] is None:
  # topCorner.flip()
while topCorner.matches[0] != None or topCorner.matches[1] != None:
  topCorner.rotate()

solution[0][0] = topCorner
topCorner.placed = True

print(f'adjusted {topCorner}')

try:

  previous_tile = topCorner
  for y in range(grid_size):
    for x in range(grid_size):
      print(f'row {y}, column {x}')
      if y == 0 and x == 0:
        #top right is already done.
        continue
        
      # search_list = middles
      # if searching_for_corner(grid_size, x, y):
      #   search_list = corners
      # elif searching_for_edge(grid_size, x, y):
      #   search_list = edges
      
      if x == 0:
        match_edge = Tile.EDGE_BOTTOM
        previous_tile = previous_tile = solution[y-1][0]
      else:
        match_edge = Tile.EDGE_RIGHT
      if y > 0:
        upper_tile_id = solution[y-1][x].id
      else:
        upper_tile_id = None
    
      search_tile_id = previous_tile.matches[match_edge]
      # found_tile = next(t for t in search_list if t.id == search_tile_id)
      found_tile = next(t for t in tiles if t.id == search_tile_id)
      print(f'found    {found_tile}')
      if found_tile.placed:
        raise StopIteration("Already Placed!!!")
      found_tile.adjust_to_match([previous_tile.id, upper_tile_id], previous_tile.edges[match_edge], opposite_edge(match_edge), calc_placement(grid_size, x, y))
      print(f'adjusted {found_tile}')

      solution[y][x] = found_tile
      previous_tile = found_tile
      found_tile.placed = True

except StopIteration:
  print_solution(solution)
  sys.exit()

debug_print(99, 'FINAL Solution:')
for y in range(grid_size):
  for x in range(grid_size):
    tile = solution[y][x]
    if tile == -1:
      tile = 'None'
    
    print(f'SOLN {x},{y}: {tile}')
   
debug_print(99,'\n\n')
debug_line_break(99)
debug_print(99, 'FINAL TILES')
for y in range(grid_size):
  for ry in range(len(topCorner.rows)):
    if ry == 0:
      for x in range(grid_size):
        print(solution[y][x].id, end='       ')
        if x+1 == grid_size:
          print('')
    for x in range(grid_size):
      end = '' if x+1 == grid_size else ' '
      print(solution[y][x].rows[ry], end=end)
    print('')
  print('')

debug_print(99,'\n\n')
debug_line_break(99)
debug_print(99, 'FINAL IMAGE')

image_array = [[-1 for i in range(int(grid_size))] for j in range(int(grid_size))]
image = ''
for y in range(grid_size):
  for x in range(grid_size):
    image_array[y][x] = solution[y][x].borderless()

for y in range(grid_size):
  for ry in range(len(image_array[0][0])):
    for x in range(grid_size):
      end = '\n' if x+1 == grid_size else ''
      print(image_array[y][x][ry], end=end)
      image += image_array[y][x][ry] + end

debug_print(99,'\n\n')
debug_line_break(99)
debug_print(99, 'FINAL IMAGE image')
print(image)