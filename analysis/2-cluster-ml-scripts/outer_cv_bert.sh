#!/bin/bash

#SBATCH --qos=short

#SBATCH --job-name=outer-cv-impacts-classifier

#SBATCH --output=outer-bert-impacts-classifier.out
#SBATCH --error=outer-bert-impacts-classifier.err
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=8

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 5 python outer_cv_bert.py -mpi 1
