#!/bin/bash
list=$(echo $1 | tr "," "\n")
for x in $list
do
	zips=(`ls -t1 "/home/gaertner/bip-data/data/voterfiles/$x/TS_Google"*".zip"`)
	if [ ${#zips[@]} == "2" ]
	then
	    rm "${zips[1]}"
	fi
done
