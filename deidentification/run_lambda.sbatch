#!/bin/bash
#SBATCH -J BP_deid
#SBATCH -p lambda-only
#SBATCH --gres=gpu:ampere:1
#SBATCH --output=lambda-%j.out
#SBATCH --error=lambda-%j.err
#SBATCH --mem=100G
#SBATCH -t 4-0:0:0

. "/home/yguo262/miniconda3/etc/profile.d/conda.sh"
conda activate /labs/sarkerlab/yguo262/conda_envs/transformers

python deid_transformers.py
