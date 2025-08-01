#!/bin/sh
#This file is called submit-script.sh
#SBATCH --partition=shared       # default "shared", if not specified
#SBATCH --time=7-00:00:00     # run time in days-hh:mm:ss
#SBATCH --nodes=1               # require 1 nodes
#SBATCH --ntasks=1                     # required number of CPUs (n)
#SBATCH --cpus-per-task=20
#SBATCH --mem-per-cpu=4000             # RAM per CPU core, in MB (default 4 GB/core)
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out
# Make sure to change the above two lines to reflect your appropriate
# file locations for standard error and output

# Now list your executable command (or a string of them).
# Example for code compiled with a software module:
module load openmpi
export OMP_NUM_THREADS=20

echo "Date:"
date '+%s'
echo "Using ACI / HCP / Slurm cluster."
echo "JobID = $SLURM_JOB_ID"
echo "Using $SLURM_NNODES nodes"
echo "Using $SLURM_NODELIST nodes."
echo "Number of cores per node: $SLURM_TASKS_PER_NODE"
echo "Submit directory: $SLURM_SUBMIT_DIR"
echo ""

##mpirun -n 20 /home/aaibrahim5/lammps-static/bin/lmp < input.lammps

echo "Finished on:"
date '+%s'

  /home/aaibrahim5/lammps-static/bin/lmp -in input.lammps


