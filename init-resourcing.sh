#! /bin/bash

function t(){
    case $1 in
	OCEAN) echo 0000CC:$2;;
	C-SEA) echo 0044FF:$2;;
	ICE-S) echo 0077FF:$2;;
	G-RIV) echo 771188:$2;;
	N-RIV) echo BB22FF:$2;;
	R-FLT) echo 33BB33:$2;;
	P-FLT) echo 55DD88:$2;;
	DESRT) echo FFEE99:$2;;
	TUNDR) echo AAAA99:$2;;
	SWAMP) echo 448844:$2;;
	PLATE) echo FFCC11:$2;;
	H-MNT) echo 884400:$2;;
	G-MNT) echo 440022:$2;;
	HILL)  echo FF4400:$2;;
	COAST) echo COAST:$2;;
	NAN) echo NAN:$2;;
    esac
}

./initiator.py -D resourcing -u 1:4 -3 -t `t COAST 0.01`-`t N-RIV 0.01`-`t G-RIV 0`-`t SWAMP 0`-`t PLATE 0`-`t HILL 0`-`t P-FLT 0`-`t H-MNT 0`-`t TUNDR 0`-`t R-FLT 0`-`t DESRT 0`-`t G-MNT 0`
./ydiagram.py -f demo.sql -D resourcing -b
