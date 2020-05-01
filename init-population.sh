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

./initiator.py -D capasity -w -10:410 -t `t COAST 6`-`t N-RIV 3`-`t G-RIV 3`-`t SWAMP 0.1`-`t PLATE 1.5`-`t HILL 0.9`-`t P-FLT 0.3`-`t H-MNT 0.1`-`t TUNDR 0.03`-`t R-FLT 8`-`t DESRT 0.03`-`t G-MNT 0.02`

# 1
./initiator.py -c -N CEL -e JTW-BHH-BMO -m 4
./initiator.py -N CEL -d EII-IWI
# ./ydiagram.py -r 2 -b -N CEL

# 2
./initiator.py -c -N SAS -e FZV -m 5
./initiator.py -N SAS -d RZW-WVI-CCD-LGE
# ./ydiagram.py -r 2 -b -N SAS

# 3
./initiator.py -c -N SLO -e FIT-BYG-DJG -m 3
# ./ydiagram.py -r 2 -b -N SLO

# 4
./initiator.py -c -N GER -e LGE-ZYQ -m 4
./initiator.py -N GER -d RCL-IPN-BJC-OET-RZW-UAG-FZV
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
./initiator.py -c -N ISM -e UAG -m 5
./initiator.py -N ISM -d XKC
# ./ydiagram.py -r 2 -b -N ISM

# 9
./initiator.py -c -N PER -e BDN-XKC -m 3
# ./ydiagram.py -r 2 -b -N PER

# 10
./initiator.py -c -N INK -e MRL-NPP-LHG -m 5
./initiator.py -N INK -d ONH-JYN-KRP-DDI-HTS-DTY
# ./ydiagram.py -r 2 -b -N INK -o 200

# 11
./initiator.py -c -N SUN -e KRP-YTV-SEL-YGE-GFN -m 4
./initiator.py -N SUN -d RKB
# ./ydiagram.py -r 2 -b -N SUN -o 200

# 12
./initiator.py -c -N JAP -e JXR-HTS-QIN -m 4
./initiator.py -N JAP -d LHG-GIE-YVR-DDI-LWL
# ./ydiagram.py -r 2 -b -N JAP -o 200

# 13
./initiator.py -c -N ZUL -e FFI-RKB -m 4
# ./ydiagram.py -r 2 -b -N ZUL -o 200

# 14
./initiator.py -c -N HAN -e YZP -m 5
./initiator.py -N HAN -d XZM-RKB-NNL-IWZ
#./ydiagram.py -r 2 -b -N HAN -o 200

# 15
./initiator.py -c -N BUD -e QZD-XZL-VFE -m 4
./initiator.py -N BUD -d VJD
# ./ydiagram.py -r 2 -b -N BUD -o 200

# 16
./initiator.py -c -N IND -e IWZ-MZC -m 4
# ./ydiagram.py -r 2 -b -N IND -o 200

./initiator.py -l # -w -10:410 -t `t COAST 6`-`t N-RIV 3`-`t G-RIV 3`-`t SWAMP 0.1`-`t PLATE 1.5`-`t HILL 0.9`-`t P-FLT 0.3`-`t H-MNT 0.1`-`t TUNDR 0.03`-`t R-FLT 8`-`t DESRT 0.03`-`t G-MNT 0.02`
./show-nations.sh
