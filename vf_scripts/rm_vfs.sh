#!/bin/bash
list=$(echo $1 | tr "," "\n")

for x in $list
do
	rm "/home/gaertner/bip-data/data/voterfiles/$x/TS_Google"*".txt"
done
