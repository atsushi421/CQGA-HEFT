#!/usr/bin/bash

# remove result
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_NumNode/NumNode_20/*.txt

# 70
python3 eval.py change_NumNode original_20_0 2 3 3 1 1 &
python3 eval.py change_NumNode original_20_1 2 3 3 1 1 &
python3 eval.py change_NumNode original_20_2 2 3 3 1 1 &
python3 eval.py change_NumNode original_20_3 2 3 3 1 1 &
python3 eval.py change_NumNode original_20_4 2 3 3 1 1 &
python3 eval.py change_NumNode original_20_5 2 3 3 1 1 &
python3 eval.py change_NumNode original_20_6 2 3 3 1 1 &
python3 eval.py change_NumNode original_20_7 2 3 3 1 1