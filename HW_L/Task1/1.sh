#!/usr/bin/env bash

dd if=/dev/sda bs=512 count=1 2>/dev/null | od -v -x -j 446 -N 64 | awk 'BEGIN { res = 0; }{
	fl = 0;
	for(j = 1; j + 1 <= NF; j++){
		if($(j + 1) != "0000"){
			fl = 1;
		}
	}
	res += fl
} 
END { print res }'