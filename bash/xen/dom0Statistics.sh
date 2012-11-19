#!/bin/bash

if [ -z "${2}" ]; then
	echo "Usage: ${0} <keyfile> <dom0>";
	exit;
fi;

server=$2;
KEY=$1;

tempDir=$(mktemp -d)

SSH="ssh -i ${KEY} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -oBatchMode=yes root@" # -o for disabling checking of fingerprint

# Executing commands on the machines
VGDISPLAY=`${SSH}${server} "vgdisplay" 2> /dev/null`;
XMINFO=`${SSH}${server} "xm info" 2> /dev/null`;
XMLIST=`${SSH}${server} "xm list" 2> /dev/null`;
LVDISPLAY=`${SSH}${server} "lvdisplay -c" 2> /dev/null`;

totalMemory=$(echo "${XMINFO}" | grep total_memory | awk -F': ' '{print $2}')
freeMemory=$(echo "${XMINFO}" | grep free_memory | awk -F': ' '{print $2}')

PEsize=$(echo "${VGDISPLAY}" | grep "PE Size" | awk '{print $3}' | sed 's/\..*//; s/\,.*//;') # last sed: casting float to integer
totalPE=$(echo "${VGDISPLAY}" | grep "Total PE" | awk '{print $3}')
allocPE=$(echo "${VGDISPLAY}" | grep "Alloc PE" | awk '{print $5}')
freePE=$(echo "${VGDISPLAY}" | grep "Free  PE" | awk '{print $5}')

echo "Dom0: ";
echo -e "total disk:\t$(($totalPE*$PEsize/1024)) GiB"
echo -e "alloc disk:\t$(($allocPE*$PEsize/1024)) GiB / $(($allocPE*100/$totalPE))%"
echo -e "free disk :\t$(($freePE*$PEsize/1024)) GiB / $(($freePE*100/$totalPE))%"
echo -e "total memory:\t${totalMemory} MiB"
echo -e "alloc memory:\t$((${totalMemory}-${freeMemory})) MiB / $(((${totalMemory}-${freeMemory})*100/$totalMemory))%"
echo -e "free memory :\t${freeMemory}  MiB / $(($freeMemory*100/$totalMemory))%";
echo "";
echo -e "DomUs:";

xens=`echo "${XMLIST}" | sed '1,2d' | awk '{print $1}'`;


for i in $LVDISPLAY; do
	name=$(echo ${i} | awk -F/ '{print $4}' | awk -F: '{print $1}')
	name=${name%-*} # gets everything but the last element splitted by "-"
	typ=$(echo ${i} | awk -F/ '{print $4}' | awk -F: '{print $1}' | awk -F- '{print $NF}')
	lvsize=$(echo ${i} | awk -F: '{print $8}')

	echo -e "xen ${typ} \t $(($lvsize*$PEsize/1024)) GiB" >> ${tempDir}/${name}.devices;
done;

for i in $xens; do
	# connecting to each machine and getting information
	DISK=`${SSH}${i} 'df -h | egrep "/$"' 2> /dev/null`;
	MEM=`${SSH}${i} 'cat /proc/meminfo' 2> /dev/null`;
	if [ -z "$DISK" ] || [ -z "${MEM}" ]; then
		echo -e "\t ->Couldn't connect" > ${tempDir}/${i}.internal;
	else
		totalDisk=$(echo $DISK | awk '{print $2}')
		usedDisk=$(echo $DISK | awk '{print $3}')
		freeDisk=$(echo $DISK | awk '{print $4}')
		percentDisk=$(echo $DISK | awk '{print $5}')
		totalMem=$(echo $MEM | awk '{print $2}') # no grep, caused it's displayed without lines
		freeMem=$(echo $MEM | awk '{print $5}') # see comment above
		echo -e "real disk \t ${totalDisk} / ${usedDisk} / ${freeDisk} -> ${percentDisk}" >> ${tempDir}/${i}.internal;
		echo -e "real ram \t ${totalMem} kb / $((${totalMem}-${freeMem})) kb / ${freeMem} kb -> $(((${totalMem}-${freeMem})*100/${totalMem}))%" >> ${tempDir}/${i}.internal;
	fi;

	echo -e "xen ram \t $(echo "${XMLIST}" | grep "${i}" | awk '{print $3}') MiB" >> ${tempDir}/${i}.ram; 
done;

for i in $xens; do
	echo "${i}";
	cat ${tempDir}/${i}.devices;
	cat ${tempDir}/${i}.ram;
	cat ${tempDir}/${i}.internal;
	echo ""
done;

rm -r "${tempDir}"
