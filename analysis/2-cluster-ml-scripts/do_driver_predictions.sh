#!/bin/bash

#SBATCH --qos=short

#SBATCH --job-name=driver-predictions

#SBATCH --output=driver-predictions.out
#SBATCH --error=driver-predictions.err
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=8

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 5 python driver_predictions_bert.py -mpi 1
