#!/bin/bash
#SBATCH -t 00:01:00
#SBATCH --mem-per-cpu=100M
#SBATCH -o debug.log
#SBATCH --array=1-2000
module load anaconda2 
source activate new_numpy 
srun python simu.py 20000 5 3 --ofile out/$SLURM_ARRAY_TASK_ID.csv
