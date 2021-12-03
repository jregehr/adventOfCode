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

#region Classes


class food:
  def __init__(self, ingredients_and_allergens):
    s_ia = ingredients_and_allergens.split(' (contains ')
    self._ingredients = set([s.strip() for s in s_ia[0].split(' ')])
    self._allergens = set([s.strip() for s in s_ia[1].replace(')', '').split(',')])
    self._non_allergen_ingredients = set()
    self._allergen_ingredients = set()

  @property
  def ingredients(self):
    return self._ingredients

  # @ingredients.setter
  # def ingredients(self, value):
  #   self._ingredients = value

  @property
  def allergens(self):
    return self._allergens

  # @allergens.setter
  # def allergens(self, value):
  #   self._allergens = value

  @property
  def non_allergen_ingredients(self):
    return self._non_allergen_ingredients

  @non_allergen_ingredients.setter
  def non_allergen_ingredients(self, value):
    self._non_allergen_ingredients = value

  @property
  def allergen_ingredients(self):
    return self._allergen_ingredients

  @allergen_ingredients.setter
  def allergen_ingredients(self, value):
    self._allergen_ingredients = value

  def print(self):
    print('--- Food Item ---')
    print(f'Ingredients: {self._ingredients}')
    print(f'Allergens: {self._allergens}')
    print(f'Allergen Ingredients: {self._allergen_ingredients}')
    print(f'Non-Allergen Ingredients: {self._non_allergen_ingredients}')

#endregion


#######################################################
debug = 0
#######################################################

foods = []
for line in lines:
  foods.append(food(line))

allergens = set()

for food in foods:
  food.print()
  allergens.update(food.allergens)

allergen_map = {}

iter = 0
while iter < 7:
  print('####################################################################################')
  print(allergens)
  iter += 1
  for allergen in allergens:
    if allergen_map.get(allergen) is not None:
      print(f'Allergen {allergen} already mapped.')
      continue
    foodsWithAllergens = [f for f in foods if allergen in f.allergens]
    if len(foodsWithAllergens) < 2:
      possible_allergen_ingredients = (foodsWithAllergens[0].ingredients - set(allergen_map.values()))
    else:
      possible_allergen_ingredients = (foodsWithAllergens[0].ingredients - set(allergen_map.values())) & (foodsWithAllergens[1].ingredients - set(allergen_map.values()))
      for x in range(2, len(foodsWithAllergens)):
        possible_allergen_ingredients = possible_allergen_ingredients & foodsWithAllergens[x].ingredients
    if len(possible_allergen_ingredients) == 1:
      allergen_map[allergen] = list(possible_allergen_ingredients)[0]

for food in foods:
  food.allergen_ingredients = food.ingredients & set(allergen_map.values())
  food.non_allergen_ingredients = food.ingredients - set(allergen_map.values())

print('####################################################################################')
non_allergen_ingredient_count = 0
for food in foods:
  # food.print()
  non_allergen_ingredient_count += len(list(food.ingredients - food.allergen_ingredients))

print(f'Ingredients without allergens appear {non_allergen_ingredient_count} times.')

allergredients = ""
for allergen in sorted(allergen_map.keys()):
  allergredients += allergen_map[allergen] + ','

print(f'canonical dangerous ingredient list: {allergredients}')
