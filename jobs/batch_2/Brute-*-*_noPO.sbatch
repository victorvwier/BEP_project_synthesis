#!/bin/sh
#SBATCH --partition=general
#SBATCH --qos=medium
#SBATCH --time=20:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=32000
#SBATCH --mail-type=FAIL

module use /opt/insy/modulefiles
module load miniconda/3.9

srun python main.py 0 0 0
srun python main.py 0 0 1
srun python main.py 0 0 2
srun python main.py 0 1 0
srun python main.py 0 1 1
srun python main.py 0 1 2
srun python main.py 0 2 0
srun python main.py 0 2 1