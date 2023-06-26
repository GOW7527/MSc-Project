#!/bin/bash
N=500
for w in 3.2 3.4 3.6 3.8 4.0 4.2 4.4 4.6 4.8 5.0 5.2 5.4 5.6 5.8
do
for tau in 0.1 0.5 1.0 1.5 2.0 2.5 3.5 4.0 4.5 5.5
do
jobname=anderson_model_w-$w-tau-$tau-N-$N
cd /home/clustor2/ma/g/gl1122/anderson/Dumps
qsub q.sh -v w=$w,tau=$tau,N=$N -N $jobname
done 
done 
