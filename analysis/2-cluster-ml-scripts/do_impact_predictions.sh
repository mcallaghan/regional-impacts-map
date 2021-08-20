#!/bin/bash

#SBATCH --qos=short

#SBATCH --job-name=impact-predictions

#SBATCH --output=impact-predictions.out
#SBATCH --error=impact-predictions.err
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=8

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 5 python impact_predictions_bert.py -mpi 1
