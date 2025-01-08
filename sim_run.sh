#!/bin/bash

# Open a new xterm terminal


seeds=(42 70 420)
num_nodes=(50 100 150)
num_bres=(0.05 0.10 0.15)
num_bizantines=(0.1 0.2 0.3 0.4)


for i in {1..10}; do
    printf "Teste $i\n"
    for num_node in "${num_nodes[@]}"; do
        for num_bre in "${num_bres[@]}"; do
            for num_bizantine in "${num_bizantines[@]}"; do
                xterm -e "python3 ./simulation.py --seed=42 --num_nodes=$num_node --num_nbr=$num_bre --num_bizantines=$num_bizantine" &
                sleep 13
                pkill -f "python3 ./simulation.py"
                xterm -e "python3 ./simulation.py --seed=70 --num_nodes=$num_node --num_nbr=$num_bre --num_bizantines=$num_bizantine" &
                sleep 13
                pkill -f "python3 ./simulation.py"
                xterm -e "python3 ./simulation.py --seed=420 --num_nodes=$num_node --num_nbr=$num_bre --num_bizantines=$num_bizantine" &
                sleep 13
                pkill -f "python3 ./simulation.py"
            done
        done
    done
done
