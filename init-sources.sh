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

# 1
# ./initiator.py -c -S GOLD -b land -u 0.2:1.1 -p 0.01 -n 2:0.2 -e QNT-CQK-VXH-BMO-NOK-FIH-LPD-QGU-XZL-DNP-RZW
# ./initiator.py  -S GOLD -b land -u 0.2:1.1 -p 0 -n 2:0.2 -e QIN
# ./ydiagram.py -r 2 -b -S GOLD

# 2
# ./initiator.py -c -S RARE -b land -u 0.1:1.5 -p 0.02 -n 1:0.3 -e GMJ-FCD-XRC-VLC-YTS-BYG-IWI-FZV-ABQ-AXL-CRK-FSO-BDN-MDN-LDH-GYW-YTU-FTA
# ./ydiagram.py -r 2 -b -S RARE

# 3
# ./initiator.py -c -S WOOD -b land -u 8.5:10.5  -w 90:360 -t `t R-FLT 0.1`-`t G-RIV 0.15`-`t N-RIV 0.1`-`t SWAMP 0.05`-`t PLATE 0.04`-`t HILL 0.03`
# ./ydiagram.py -r 2 -b -S WOOD

# 4
# ./initiator.py -c -S STONE -b land -u 8.5:10.5  -t `t G-MNT 0.2`-`t H-MNT 0.2`-`t COAST 0.03`-`t HILL 0.1`-`t DESRT 0.02`-`t PLATE 0.01`
# ./ydiagram.py -r 2 -b -S STONE

# 5
# ./initiator.py -c -S FISH -u 5.5:6.5 -w -10:410 -t `t COAST 0.1`-`t N-RIV 0.3`-`t G-RIV 0.2`-`t OCEAN 0.02`-`t C-SEA 0.035`-`t ICE-S 0.01`
# ./ydiagram.py -r 2 -b -S FISH

# 6
# ./initiator.py -c -S AGRA -b land -u 8.5:10.5  -w 55:370 -t `t R-FLT 0.1`-`t G-RIV 0.05`-`t N-RIV 0.08`-`t SWAMP 0.01`-`t PLATE 0.04`-`t HILL 0.03`-`t P-FLT 0.02`-`t H-MNT 0.005`-`t TUNDR 0.002`
# ./ydiagram.py -r 2 -b -S AGRA

# 7
# ./initiator.py -c -S REVE -b land -u 2.5:3.5  -t `t COAST 0.1`-`t N-RIV 0.3`-`t G-RIV 0.2`-`t HILL 0.15`-`t H-MNT 0.1`-`t PLATE 0.15`-`t P-FLT 0.1`-`t DESRT 0.1`-`t R-FLT 0.03`-`t TUNDR 0.1`
# ./ydiagram.py -r 2 -b -S REVE

# 8
# ./initiator.py -c -S ORE -b land -u 8.5:9.5 -p 0.1 -n 1:0.4 -t `t R-FLT 0.8`-`t PLATE 0.4`-`t HILL 0.3`-`t P-FLT 0.2`-`t H-MNT 0.5`-`t TUNDR 0.2`-`t DESRT 0.3`-`t G-MNT 0.4` -e NBV-UEF-VJD-IWZ-ILO-GDM-PKZ-LTH-KJZ-LWL-SUI-KRP
# ./ydiagram.py -r 2 -b -S ORE

# 9
# ./initiator.py -c -S COAL -b land -u 200.5:950.5 -p 0.12 -n 1:0.4  -e BIW-UAE-JJA-ZYQ-DDI-NOK-XJC-PKZ-MLT-NGF-IWI-IPN-RCL
# ./ydiagram.py -r 2 -b -S COAL

# 10
# ./initiator.py -c -S OIL -u 400.5:1350.5 -p 0.04 -n 5:0.4  -t `t OCEAN 0`-`t G-MNT 0`-`t NAN 1` -e CGR-MUO-RZW-BHH-UEM-BFP-DTY-XZL-GDV-COD-SVI
# ./ydiagram.py -r 2 -b -S OIL





