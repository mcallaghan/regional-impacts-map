#!/bin/bash

#SBATCH --qos=short

#SBATCH --job-name=cv-svm-impacts

#SBATCH --output=cv-svm-impacts.out
#SBATCH --error=cv-svm-impacts.err
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=8

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 3 python cv_svm_impacts.py -mpi 1
