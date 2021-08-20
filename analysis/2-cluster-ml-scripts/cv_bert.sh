#!/bin/bash

#SBATCH --qos=medium

#SBATCH --job-name=cv-impacts-classifier-cputask

#SBATCH --output=bert-impacts-classifier.out
#SBATCH --error=bert-impacts-classifier.err
#SBATCH --ntasks=25
#SBATCH --cpus-per-task=8


source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 25 python cv_bert.py -mpi 1
