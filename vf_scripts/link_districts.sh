#!/bin/bash
list=$(echo $1 | tr "," "\n")

for x in $list
do
	mkdir "/home/gaertner/bip-data/districts/$x"
	cp "/home/gaertner/bip-data/data/voterfiles/$x/districts.py" "/home/gaertner/bip-data/districts/$x/districts.py"
done
