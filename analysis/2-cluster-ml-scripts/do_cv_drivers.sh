#!/bin/bash

#SBATCH --qos=medium

#SBATCH --job-name=cv-multilabel-drivers

#SBATCH --output=cv-multilabel-drivers.out
#SBATCH --error=cv-multilabel-drivers.err
#SBATCH --ntasks=9
#SBATCH --cpus-per-task=8
#SBATCH --time=2-0

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 9 python cv_bert_drivers.py -mpi 1
