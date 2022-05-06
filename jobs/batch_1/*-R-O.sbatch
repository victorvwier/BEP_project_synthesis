#!/bin/sh
#SBATCH --partition=general
#SBATCH --qos=short
#SBATCH --time=0:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=32000
#SBATCH --mail-type=END

module use /opt/insy/modulefiles
module load miniconda/3.9

srun python main.py 0 1 2
srun python main.py 1 1 2
srun python main.py 2 1 2
srun python main.py 3 1 2
srun python main.py 4 1 2
srun python main.py 5 1 2