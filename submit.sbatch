#!/bin/bash
#SBATCH -t 02:00:00
#SBATCH --mem-per-cpu=100M
#SBATCH -o debug.log
#SBATCH --array=1-23988
module load anaconda2 
source activate new_numpy 
srun python simu.py < jobs/$SLURM_ARRAY_TASK_ID.in 
