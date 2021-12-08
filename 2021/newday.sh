#!/bin/bash

if [ "$1" == "" ]; then
  echo "Provide a day number."
  exit 1
fi

dayName="day-$1"

mkdir -p $dayName
touch $dayName/README.md
touch $dayName/small.txt
touch $dayName/input.txt
# This doesn't work because you have to be logged in
#curl -s "https://adventofcode.com/2021/day/${1/#+(0)/}/input" -o $dayName/input.txt
cp ./template/answerTemplate.py $dayName/solution.py

code $dayName/solution.py $dayName/small.txt