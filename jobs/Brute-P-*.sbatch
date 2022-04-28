#!/bin/sh
#SBATCH --partition=general
#SBATCH --qos=short
#SBATCH --time=2:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=32000
#SBATCH --mail-type=END

module use /opt/insy/modulefiles
module load miniconda/3.9

srun python main.py 0 2 0
srun python main.py 0 2 1
srun python main.py 0 2 2