#!/bin/bash
list=$(echo $1 | tr "," "\n")

for x in $list
do
	ln -s "/home/gaertner/bip-data/data/voterfiles/$x/out" "/home/gaertner/Dropbox/BIP Production/candidate_to_ed_tables/$x"
done
