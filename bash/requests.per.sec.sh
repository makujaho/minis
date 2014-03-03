#!/bin/sh

usage="Usage: `basename $0` -f <frequency in seconds, min 1, default 60> -l <log file>"

# Set up options
while getopts ":l:f:" options; do
 case $options in
 l ) logFile=$OPTARG;;
 f ) frequency=$OPTARG;;
 \? ) echo -e $usage
  exit 1;;
 * ) echo -e $usage
  exit 1;;

 esac
done

# Test for logFile
if [  ! -n "$logFile" ]
then
 echo -e $usage
 exit 1
fi

# Test for frequency
if [  ! -n "$frequency" ]
then
 frequency=60
fi

# Test that frequency is an integer
if [  $frequency -eq $frequency 2> /dev/null ]
then
 :
else
 echo -e $usage
 exit 3
fi

# Test that frequency is an integer
if [  $frequency -lt 1 ]
then
 echo -e $usage
 exit 3
fi

if [ ! -e "$logFile" ]
then
 echo "$logFile does not exist."
 echo 
 echo -e $usage
 exit 2
fi

lastCount=$(wc -l $logFile | sed 's/\([0-9]*\).*/\1/')
while true
do
 newCount=$(wc -l $logFile | sed 's/\([0-9]*\).*/\1/')
 diff=$(( newCount - lastCount ))
 rate=$(echo "scale=2; $diff / $frequency" |bc -l)
 echo $(date) " " $rate
 lastCount=$newCount
 sleep $frequency
done
