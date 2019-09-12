#! /bin/bash

# 1
./initiator.py -c -N CEL -e JTW-BHH-BMO -m 4
./initiator.py -N CEL -d EII
# ./ydiagram.py -r 2 -b -N CEL

# 2
./initiator.py -c -N SAS -e FZV -m 5
./initiator.py -N SAS -d RZW
# ./ydiagram.py -r 2 -b -N SAS

# 3
./initiator.py -c -N SLO -e FIT-BYG -m 3
# ./ydiagram.py -r 2 -b -N SLO

# 4
./initiator.py -c -N GER -e LGE-ZYQ -m 4
./initiator.py -N GER -d RCL-IPN-BJC-OET-RZW-UAG
# ./ydiagram.py -r 2 -b -N GER

# 5
./initiator.py -c -N LAT -e DKC-OLT-WVI -m 3
# ./ydiagram.py -r 2 -b -N LAT

# 6
./initiator.py -c -N NOR -e GEW-QON-LGJ -m 4
./initiator.py -N NOR -d XKC
# ./ydiagram.py -r 2 -b -N NOR

# 7
./initiator.py -c -N TUR -e RCL-XYZ -m 3
./initiator.py -N TUR -d BYG-GFM
# ./ydiagram.py -r 2 -b -N TUR

# 8
./initiator.py -c -N ISM -e UAG -m 4
# ./ydiagram.py -r 2 -b -N ISM

# 9
./initiator.py -c -N PER -e BDN-XKC -m 3
# ./ydiagram.py -r 2 -b -N PER




# 10
./initiator.py -c -N INK -e MRL-NPP-LHG -m 5
./initiator.py -N INK -d ONH-JYN-KRP-DDI
# ./ydiagram.py -r 2 -b -N INK -o 200

# 11
./initiator.py -c -N SUN -e KRP-YTV-SEL -m 4
# ./ydiagram.py -r 2 -b -N SUN -o 200

# 12
./initiator.py -c -N JAP -e JXR-JYN-HTS -m 3
# ./ydiagram.py -r 2 -b -N JAP -o 200

# 13
./initiator.py -c -N ZUL -e FFI -m 4
# ./ydiagram.py -r 2 -b -N ZUL -o 200

# 14
./initiator.py -c -N HAN -e YZP -m 4
./initiator.py -N HAN -d MMU-NFY-XZM
#./ydiagram.py -r 2 -b -N HAN -o 200

# 15
./initiator.py -c -N BUD -e QZD-XZL-VFE -m 4
# ./ydiagram.py -r 2 -b -N BUD -o 200

# 16
./initiator.py -c -N HIN -e IWZ-MZC -m 4
# ./ydiagram.py -r 2 -b -N HIN -o 200


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

./initiator.py -l -w -10:410 -t `t COAST 6`-`t N-RIV 3`-`t G-RIV 3`-`t SWAMP 0.1`-`t PLATE 2`-`t HILL 1`-`t P-FLT 1`-`t H-MNT 0.2`-`t TUNDR 0.06`-`t R-FLT 8`-`t DESRT 0.06`-`t G-MNT 0.04`
./ydiagram.py -r 2 -b -P -N SAS:255:0:0-CEL:0:0:255-GER:0:128:0-LAT:255:128:0-PER:0:180:180-ISM:255:0:255-NOR:0:0:128-TUR:255:255:0-SLO:128:0:0-INK:255:128:128-JAP:0:255:0-SUN:0:80:80-ZUL:128:0:128-HAN:255:60:60-HIN:128:64:0-BUD:64:128:255
# ./ydiagram.py -r 2 -b -P
