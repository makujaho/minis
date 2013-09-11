for i in $(cat serverip.txt);
do
    ping -c 1 -W 1 $i > /dev/null && { echo "** ${i} Online";ON=$(($ON+1)); } || { echo "!! ${i} Offline";OF=$(($OF+1)); };
done;
echo "Es sind ${ON} Server online und ${OF} Server offline"
