#!/bin/bash

#SBATCH --qos=short

#SBATCH --job-name=cv-svm-impacts-classifier

#SBATCH --output=svm-cv-impacts-classifier.out
#SBATCH --error=svm-cv-impacts-classifier.err
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=8

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 5 python cv_svm.py -mpi 1
