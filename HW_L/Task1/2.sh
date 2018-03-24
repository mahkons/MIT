#!/usr/bin/env bash

for line in $(dd if=/dev/sda bs=512 count=1 2>/dev/null | od -v -x -j 446 -N 64 | awk '{ 
	if(NF >= 4)
		print toupper(substr($4, 1, 2))
}'); do
	if [[ "$line" != "00" ]]; then 
		reg=\^$line\(\.\*\)\$
		grep -E "$reg" MBR_Table
	fi
done