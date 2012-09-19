#!/bin/bash
list=$(echo $1 | tr "," "\n")

for x in $list
do
	mv "/home/gaertner/bip-data/data/voterfiles/$x/vf_compressed" "/home/gaertner/bip-data/data/voterfiles/$x/vf_compressed_cut"
done
