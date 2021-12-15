#!/usr/bin/bash

# remove result
# rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_CCR/CCR_0.25/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_CCR/CCR_0.5/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_CCR/CCR_1.0/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_CCR/CCR_2.0/*.txt
rm /mnt/c/Users/atsushi/Documents/study/M1/IPSJ/RL/Code/result/change_CCR/CCR_4.0/*.txt

# CCR 0.25
# python3 eval.py change_CCR original_50_0 2 3 3 0.8 2 &
# python3 eval.py change_CCR original_50_1 2 3 3 0.8 2 &
# python3 eval.py change_CCR original_50_2 2 3 3 0.8 2 &
# python3 eval.py change_CCR original_50_3 2 3 3 0.8 2 &
# python3 eval.py change_CCR original_50_4 2 3 3 0.8 2 &
# python3 eval.py change_CCR original_50_5 2 3 3 0.8 2 &
# python3 eval.py change_CCR original_50_6 2 3 3 0.8 2 &
# python3 eval.py change_CCR original_50_7 2 3 3 0.8 2
# wait

# CCR 0.5
python3 eval.py change_CCR original_50_0 2 3 3 1 1.3 &
python3 eval.py change_CCR original_50_1 2 3 3 1 1.3 &
python3 eval.py change_CCR original_50_2 2 3 3 1 1.3 &
python3 eval.py change_CCR original_50_3 2 3 3 1 1.3 &
python3 eval.py change_CCR original_50_4 2 3 3 1 1.3 &
python3 eval.py change_CCR original_50_5 2 3 3 1 1.3 &
python3 eval.py change_CCR original_50_6 2 3 3 1 1.3 &
python3 eval.py change_CCR original_50_7 2 3 3 1 1.3
wait

# CCR 1.0
python3 eval.py change_CCR original_50_0 2 3 3 1.5 1 &
python3 eval.py change_CCR original_50_1 2 3 3 1.5 1 &
python3 eval.py change_CCR original_50_2 2 3 3 1.5 1 &
python3 eval.py change_CCR original_50_3 2 3 3 1.5 1 &
python3 eval.py change_CCR original_50_4 2 3 3 1.5 1 &
python3 eval.py change_CCR original_50_5 2 3 3 1.5 1 &
python3 eval.py change_CCR original_50_6 2 3 3 1.5 1 &
python3 eval.py change_CCR original_50_7 2 3 3 1.5 1
wait

# CCR 2.0
python3 eval.py change_CCR original_50_0 2 3 3 2 0.7 &
python3 eval.py change_CCR original_50_1 2 3 3 2 0.7 &
python3 eval.py change_CCR original_50_2 2 3 3 2 0.7 &
python3 eval.py change_CCR original_50_3 2 3 3 2 0.7 &
python3 eval.py change_CCR original_50_4 2 3 3 2 0.7 &
python3 eval.py change_CCR original_50_5 2 3 3 2 0.7 &
python3 eval.py change_CCR original_50_6 2 3 3 2 0.7 &
python3 eval.py change_CCR original_50_7 2 3 3 2 0.7
wait

# CCR 4.0
python3 eval.py change_CCR original_50_0 2 3 3 3 0.5 &
python3 eval.py change_CCR original_50_1 2 3 3 3 0.5 &
python3 eval.py change_CCR original_50_2 2 3 3 3 0.5 &
python3 eval.py change_CCR original_50_3 2 3 3 3 0.5 &
python3 eval.py change_CCR original_50_4 2 3 3 3 0.5 &
python3 eval.py change_CCR original_50_5 2 3 3 3 0.5 &
python3 eval.py change_CCR original_50_6 2 3 3 3 0.5 &
python3 eval.py change_CCR original_50_7 2 3 3 3 0.5