import sys
import os
import abc
import array as arr

# region DiskItem

class aDiskItem:
  @abc.abstractmethod
  def itemType(self):
    pass

  @abc.abstractmethod
  def toStr(self, prefix=""):
    pass

  @abc.abstractmethod
  def name(self):
    pass

  @abc.abstractmethod
  def size(self):
    pass

# endregion

# region File

class aFile(aDiskItem):
  ITEM_TYPE = "file"

  def __init__(self, name, size=0):
    self._name = name
    self._size = size

  @property
  def name(self):
    return self._name

  @property
  def size(self):
    return self._size

  @property
  def itemType(self):
    return self.ITEM_TYPE
  
  def toStr(self, prefix=""):
    return prefix + self._name + " (size: " + str(self._size) + ")\n"

# endregion

# region Directory

class aDirectory(aDiskItem):
  ITEM_TYPE = "directory"

  def __init__(self, name, parent=None):
    self._name = name
    self._parent = parent
    self._items = [] #arr.array('aDiskItem', [])
  
  @property
  def name(self):
    return self._name

  @property
  def parent(self):
    return self._parent

  @property
  def items(self):
    return self._items

  @property
  def itemType(self):
    return self.ITEM_TYPE
  
  @property
  def size(self):
    result = 0
    for item in self._items:
      result += item.size
    return result
  
  def switch(self, dirName):
    if dirName == "..":
      return self if self._parent == None else self._parent
    
    for item in self._items:
      if item._name == dirName:
        return item
    
    return self
  
  def _sortItems(self):
    self._items.sort(key=name)

  def addFile(self, name, size):
    newFile = aFile(name, size)
    self._items.append(newFile)
    self._sortItems
    return newFile
  
  def addDirectory(self, name):
    newDir = aDirectory(name, self)
    self._items.append(newDir)
    self._sortItems
    return newDir

  def toStr(self, prefix=""):
    result = prefix + self._name + "   (treeSize: " + str(self.treeSize()) + ") \n"
    if prefix == "":
      prefix = "├──"
    else:
      prefix = "   " + prefix
    for item in self._items:
      result += item.toStr(prefix)
    return result

  def treeSize(self):
    size = 0
    for i in self._items:
      if aFile.ITEM_TYPE == i.itemType:
        size += i.size
      else:
        size += i.treeSize()
    return size

  def treeSizes(self):
    mysize = self.treeSize()
    for i in self._items:
      if aDirectory.ITEM_TYPE == i.itemType:
        yield from i.treeSizes()
    yield mysize


# endregion


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

root = aDirectory("/")
curDir = root

allDirs = [] #arr.array('aDirectory', [])

for l in lines:
  # print(f'line: {l}')
  la = l.split(' ')

  if la[0] == "$":
    if la[1] == "ls":
      continue
    # la[1] = cd
    if la[2] == "..":
      curDir = curDir.parent
      continue
    if la[2] == "/":
      curDir = root
      continue
    #cd into a dir
    curDir = curDir.switch(la[2])
    continue

  if la[0] == "dir":
    newDir = curDir.addDirectory(la[1]) 
    allDirs.append(newDir)
  else:
    curDir.addFile(la[1], int(la[0]))
    

# print(root.toStr())

totals = 0

print(root.treeSizes())
for i in root.treeSizes():
  if i <= 100000:
    totals += i
  print(i)

print(f'total: {totals}')

allDirs.sort(key=lambda d: d.size)

allDisk = 70000000
needFree = 30000000

usedDisk = root.treeSize()
unusedDisk = allDisk - usedDisk

needToFree = needFree - unusedDisk

print(f'allDisk: {allDisk}')
print(f'needFree: {needFree}')
print(f'usedDisk: {usedDisk}')
print(f'unusedDisk: {unusedDisk}')
print(f'needToFree: {needToFree}')


for d in allDirs:
  if d.treeSize() >= needToFree:
    print(f'You can delete {d.name}, it is {d.treeSize()}')
    break