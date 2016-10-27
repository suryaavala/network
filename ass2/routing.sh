#!/bin/bash

trap 'kill $(jobs -p)' SIGINT SIGTERM EXIT

# python3 Lsr.py A 2000 ./Topology1/configA.txt > ./output/outputA.txt &
#
#
# python3 Lsr.py B 2001 ./Topology1/configB.txt > ./output/outputB.txt &
#
#
# python3 Lsr.py C 2002 ./Topology1/configC.txt > ./output/outputC.txt &
#
# python3 Lsr.py D 2003 ./Topology1/configD.txt > ./output/outputD.txt &
#
# python3 Lsr.py E 2004 ./Topology1/configE.txt > ./output/outputE.txt &
#
# python3 Lsr.py F 2005 ./Topology1/configF.txt > ./output/outputF.txt &



python3 Lsr.py A 2000 ./Topology1/configA.txt &


python3 Lsr.py B 2001 ./Topology1/configB.txt &


python3 Lsr.py C 2002 ./Topology1/configC.txt &

python3 Lsr.py D 2003 ./Topology1/configD.txt &

python3 Lsr.py E 2004 ./Topology1/configE.txt &

python3 Lsr.py F 2005 ./Topology1/configF.txt &

sleep 60
