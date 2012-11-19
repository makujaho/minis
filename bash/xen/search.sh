#!/bin/bash
servers=(); # list of servers
SEARCH=${1}
KEY="aaa"; # key for keylogin (root login mandatory for the moment
SSH="ssh -i ${KEY} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -oBatchMode=yes root@"
for i in ${servers[@]}; do
	XMLIST=`${SSH}${i} "xm list" 2> /dev/null`;

	if echo ${XMLIST} | grep "${SEARCH}" > /dev/null; then
		echo "${i}: ";
		xens=`echo "${XMLIST}" | sed '1,2d' | awk '{print $1}'`;
		for a in $xens; do
			if echo "${a}" | grep "${SEARCH}" > /dev/null; then
				echo -e "\t${a}"
			fi
		done;
	fi;
done;
