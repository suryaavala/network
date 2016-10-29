#!/bin/bash
xterm -geometry 53x19+0+0 -e "python3 ../Lsr.py A 1025 configA.txt" &
echo "A,$!" >> pid.txt
xterm -geometry 53x19+480+0 -e "python3 ../Lsr.py B 1026 configB.txt" &
echo "B,$!" >> pid.txt
xterm -geometry 53x19+960+0 -e "python3 ../Lsr.py C 1027 configC.txt" &
echo "C,$!" >> pid.txt
xterm -geometry 53x19+0+293 -e "python3 ../Lsr.py D 1028 configD.txt" &
echo "D,$!" >> pid.txt
xterm -geometry 53x19+480+293 -e "python3 ../Lsr.py E 1029 configE.txt" &
echo "E,$!" >> pid.txt
xterm -geometry 53x19+960+293 -e "python3 ../Lsr.py F 1030 configF.txt" &
echo "F,$!" >> pid.txt
xterm -geometry 53x19+960+586 -e "bash ../show_graph.sh graph.txt pid.txt"
rm pid.txt
