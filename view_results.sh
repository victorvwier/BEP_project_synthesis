#!/bin/sh

pixel_brute=$(ls -1 ./results/pixel/ | grep brute)
robot_brute=$(ls -1 ./results/robot/ | grep brute)
string_brute=$(ls -1 ./results/string/ | grep brute)

pixel_gp=$(ls -1 ./results/pixel/ | grep gp)
robot_gp=$(ls -1 ./results/robot/ | grep gp)
string_gp=$(ls -1 ./results/string/ | grep gp)

rm -rf ./plots
mkdir ./plots
some_stats=$(/bin/python3 process_results_vanilla_GP.py $pixel_gp $robot_gp $string_gp $pixel_brute $robot_brute $string_brute)
echo "$some_stats" >> ./plots/some_stats.txt
