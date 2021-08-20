#!/bin/bash

#SBATCH --qos=short

#SBATCH --job-name=outer-cv-impacts

#SBATCH --output=outer-cv-impacts.out
#SBATCH --error=outer-cv-impacts.err
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=8
#SBATCH --time=2:0:0

source activate hft

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun --mpi=pmi2 -n 3 python outer_cv_bert_impacts.py -mpi 1
