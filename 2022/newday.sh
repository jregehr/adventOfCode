#!/bin/bash

if [ "$1" == "" ]; then
  echo "Provide a day number."
  exit 1
fi
dayNum=$(printf "%02d" $1)
echo "making day-${dayNum}..."
dayName="day-${dayNum}"

cookie="session=53616c7465645f5fab233359295ffb97e67b2d6a1df61f5d379f76d28f4b85b612e79cdca2f66c239960fbe5c2ef1edb59e1124f8e700a173cd89c07249e626c"

mkdir -p $dayName
touch $dayName/README.md
touch $dayName/small.txt
touch $dayName/input.txt

# This doesn't work because you have to be logged in
curl -s "https://adventofcode.com/2022/day/${1}/input" --cookie $cookie  -o $dayName/input.txt

head -30 $dayName/input.txt > $dayName/small.txt

cp ./template/answerTemplate.py $dayName/solution.py

code $dayName/solution.py $dayName/small.txt

cd $dayName
