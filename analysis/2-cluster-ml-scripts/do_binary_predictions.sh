#!/bin/bash

#SBATCH --qos=medium

#SBATCH --job-name=predictions-impacts-classifier

#SBATCH --output=predictions-impacts-classifier.out
#SBATCH --error=predictions-impacts-classifier.err
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=8
#SBATCH --time=2-0


source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 10 python binary_predictions_bert.py -mpi 1
