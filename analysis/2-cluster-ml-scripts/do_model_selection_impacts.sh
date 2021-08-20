#!/bin/bash

#SBATCH --qos=medium

#SBATCH --job-name=model-selection-impacts

#SBATCH --output=model-selection-impacts.out
#SBATCH --error=model-selection-impacts.err
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=8
#SBATCH --time=2-0


source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 3 python model_selection_impacts.py -mpi 1
