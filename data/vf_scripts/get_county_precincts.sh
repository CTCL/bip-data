#!/bin/bash
cut -f 21,22,28,29 "/home/gaertner/bip-data/data/voterfiles/$1/vf_compressed" | grep -i "$2" | sort -u | grep -n '' | tr ':\t' ',,' 
