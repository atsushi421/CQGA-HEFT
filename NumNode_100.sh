#!/usr/bin/bash

# remove result
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_NumNode/NumNode_100/*.txt

# 100
python3 eval.py change_NumNode original_100_0 2 3 3 1 1 &
python3 eval.py change_NumNode original_100_1 2 3 3 1 1 &
python3 eval.py change_NumNode original_100_2 2 3 3 1 1 &
python3 eval.py change_NumNode original_100_3 2 3 3 1 1 &
python3 eval.py change_NumNode original_100_4 2 3 3 1 1 &
python3 eval.py change_NumNode original_100_5 2 3 3 1 1 &
python3 eval.py change_NumNode original_100_6 2 3 3 1 1 &
python3 eval.py change_NumNode original_100_7 2 3 3 1 1