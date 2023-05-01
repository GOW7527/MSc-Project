#!/bin/bash
#PBS -m bea
#PBS -q standard
cd /home/clustor2/ma/g/gl1122/anderson
python3 anderson_model.py --w $w --t $tau --n $N
