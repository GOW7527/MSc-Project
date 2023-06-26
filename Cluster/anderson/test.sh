#!/bin/bash
N=500
for w in 0.1 
do
for tau in 1.0 
do
jobname=decay_w-$w-tau-$tau-N-$N
cd /home/clustor2/ma/g/gl1122/anderson/Dumps
qsub q.sh -v w=$w,tau=$tau,N=$N -N $jobname
done 
done 