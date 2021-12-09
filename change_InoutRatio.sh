#!/usr/bin/bash

# remove result
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_InoutRatio/InoutRatio_1.5/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_InoutRatio/InoutRatio_3.0/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_InoutRatio/InoutRatio_6.0/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_InoutRatio/InoutRatio_12.0/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_InoutRatio/InoutRatio_24.0/*.txt

# InoutRatio_1.5
python3 eval.py change_InoutRatio new_50_0 2 3 1.5 1 1 &
python3 eval.py change_InoutRatio new_50_1 2 3 1.5 1 1 &
python3 eval.py change_InoutRatio new_50_2 2 3 1.5 1 1 &
python3 eval.py change_InoutRatio new_50_3 2 3 1.5 1 1 &
python3 eval.py change_InoutRatio new_50_4 2 3 1.5 1 1 &
python3 eval.py change_InoutRatio new_50_5 2 3 1.5 1 1 &
python3 eval.py change_InoutRatio new_50_6 2 3 1.5 1 1 &
python3 eval.py change_InoutRatio new_50_7 2 3 1.5 1 1
wait

# InoutRatio_3.0
python3 eval.py change_InoutRatio new_50_0 2 3 3.0 1 1 &
python3 eval.py change_InoutRatio new_50_1 2 3 3.0 1 1 &
python3 eval.py change_InoutRatio new_50_2 2 3 3.0 1 1 &
python3 eval.py change_InoutRatio new_50_3 2 3 3.0 1 1 &
python3 eval.py change_InoutRatio new_50_4 2 3 3.0 1 1 &
python3 eval.py change_InoutRatio new_50_5 2 3 3.0 1 1 &
python3 eval.py change_InoutRatio new_50_6 2 3 3.0 1 1 &
python3 eval.py change_InoutRatio new_50_7 2 3 3.0 1 1
wait

# InoutRatio_6.0
python3 eval.py change_InoutRatio new_50_0 2 3 6.0 1 1 &
python3 eval.py change_InoutRatio new_50_1 2 3 6.0 1 1 &
python3 eval.py change_InoutRatio new_50_2 2 3 6.0 1 1 &
python3 eval.py change_InoutRatio new_50_3 2 3 6.0 1 1 &
python3 eval.py change_InoutRatio new_50_4 2 3 6.0 1 1 &
python3 eval.py change_InoutRatio new_50_5 2 3 6.0 1 1 &
python3 eval.py change_InoutRatio new_50_6 2 3 6.0 1 1 &
python3 eval.py change_InoutRatio new_50_7 2 3 6.0 1 1
wait

# InoutRatio_12.0
python3 eval.py change_InoutRatio new_50_0 2 3 12.0 1 1 &
python3 eval.py change_InoutRatio new_50_1 2 3 12.0 1 1 &
python3 eval.py change_InoutRatio new_50_2 2 3 12.0 1 1 &
python3 eval.py change_InoutRatio new_50_3 2 3 12.0 1 1 &
python3 eval.py change_InoutRatio new_50_4 2 3 12.0 1 1 &
python3 eval.py change_InoutRatio new_50_5 2 3 12.0 1 1 &
python3 eval.py change_InoutRatio new_50_6 2 3 12.0 1 1 &
python3 eval.py change_InoutRatio new_50_7 2 3 12.0 1 1
wait

# InoutRatio_24.0
python3 eval.py change_InoutRatio new_50_0 2 3 24.0 1 1 &
python3 eval.py change_InoutRatio new_50_1 2 3 24.0 1 1 &
python3 eval.py change_InoutRatio new_50_2 2 3 24.0 1 1 &
python3 eval.py change_InoutRatio new_50_3 2 3 24.0 1 1 &
python3 eval.py change_InoutRatio new_50_4 2 3 24.0 1 1 &
python3 eval.py change_InoutRatio new_50_5 2 3 24.0 1 1 &
python3 eval.py change_InoutRatio new_50_6 2 3 24.0 1 1 &
python3 eval.py change_InoutRatio new_50_7 2 3 24.0 1 1