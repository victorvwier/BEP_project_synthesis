#!/bin/sh
#SBATCH --partition=general
#SBATCH --qos=short
#SBATCH --time=2:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --mem=128000
#SBATCH --mail-type=END

module use /opt/insy/modulefiles
module load miniconda/3.9

srun python main.py
