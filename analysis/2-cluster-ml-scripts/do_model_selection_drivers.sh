#!/bin/bash

#SBATCH --qos=medium

#SBATCH --job-name=model-selection-drivers

#SBATCH --output=model-selection-drivers.out
#SBATCH --error=model-selection-drivers.err
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=8
#SBATCH --time=2-0


source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 3 python model_selection_drivers.py -mpi 1
