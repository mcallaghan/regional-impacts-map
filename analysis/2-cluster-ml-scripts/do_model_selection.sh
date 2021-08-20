#!/bin/bash

#SBATCH --qos=medium

#SBATCH --job-name=model-selection-impacts-classifier

#SBATCH --output=model-selection-impacts-classifier.out
#SBATCH --error=model-selection-impacts-classifier.err
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=8

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 5 python model_selection.py -mpi 1
