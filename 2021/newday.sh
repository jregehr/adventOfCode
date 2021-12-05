#!/bin/bash

if [ "$1" == "" ]; then
  echo "Provide a day number."
  exit 1
fi

dayName="day-$1"

mkdir -p $dayName
touch $dayName/README.md
touch $dayName/small.txt
cp ./template/answerTemplate.py $dayName/solution.py

shopt -s extglob

echo "https://adventofcode.com/2021/day/${1/#+(0)/}/input"
curl -s "https://adventofcode.com/2021/day/${1/#+(0)/}/input" -o $dayName/input.txt