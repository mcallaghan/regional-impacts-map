#!/bin/bash

#SBATCH --qos=short

#SBATCH --job-name=outer-cv-drivers

#SBATCH --output=outer-cv-drivers.out
#SBATCH --error=outer-cv-drivers.err
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=8
#SBATCH --time=1:0:0

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 3 python outer_cv_bert_drivers.py -mpi 1
