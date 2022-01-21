#!/bin/sh

pixel_brute=$(ls -1 ./results/pixel/ | grep brute)
robot_brute=$(ls -1 ./results/robot/ | grep brute)
string_brute=$(ls -1 ./results/string/ | grep brute)

pixel_gp=$(ls -1 ./results/pixel/ | grep gp)
robot_gp=$(ls -1 ./results/robot/ | grep gp)
string_gp=$(ls -1 ./results/string/ | grep gp)

module use /opt/insy/modulefiles
module load miniconda/3.9

some_stats=$(python process_results_vanilla_GP.py $pixel_brute $robot_brute $string_brute $pixel_gp $robot_gp $string_gp)
echo "$some_stats" >> ./Plots/some_stats.txt
