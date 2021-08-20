#!/bin/bash

#SBATCH --qos=medium

#SBATCH --job-name=cv-multilabel-impacts

#SBATCH --output=cv-multilabel-impacts.out
#SBATCH --error=cv-multilabel-impacts.err
#SBATCH --ntasks=9
#SBATCH --cpus-per-task=8
#SBATCH --time=2-0

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 9 python cv_bert_multilabel_all.py -mpi 1
