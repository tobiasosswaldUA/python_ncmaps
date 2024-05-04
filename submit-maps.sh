#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=00:40:00
#SBATCH --mem=64G
#SBATCH --partition=short
#SBATCH --mail-type=ALL
#SBATCH --mail-user=tobiasosswald@ua.pt
#SBATCH --job-name=ncPlots
#SBATCH --no-requeue

####################################
# para submeter este ficheiro:
# sbatch submit-chimere.sh
####################################

echo "Current working directory is `pwd`"
echo "Current python3 is `which python3`"

cd /CESAM/GEMAC2/tobias/python_ncmaps 

for RUN in {26..31}; do
    echo RUN = $RUN
    cat concentration_maps.py | sed 's/__RUN__/'"${RUN}"'/' > concentration_maps_run.py
    python3 concentration_maps_run.py
    echo " "
done

exit
