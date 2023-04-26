#!/bin/bash
#PBS -m bea
#PBS -q standard
cd ${HOME}/off_diagonal
python3 off_diagonal.py --sd $sd --t $tau --n $N
