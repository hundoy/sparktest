#!/bin/bash

run_num=0
#for uid in 3896988743 3018581901 1732185795 5817914522 5075471701 6099551993 2878662450 5245892628 2071986990 5509235726
for uid in 2155714654 2514178642 5680252185 6415497685 6119605928 1724564747 2061074671 5645184348 5694525385 5341816627 5362445711 5659658830 1993311637 5299568490 5535512132 
do
echo $uid
python -u /home/zohar/py/weiboSpider.py ${uid} > /home/zohar/py/logs/${uid}.log &
rum_num=`ps aux | grep weiboSpider | wc -l`
while [[ $rum_num -gt 3 ]]
do
  echo "BIG let's hang!"
  sleep 2s
  rum_num=`ps aux | grep weiboSpider | wc -l`
done
done

wait

echo "all over!"

