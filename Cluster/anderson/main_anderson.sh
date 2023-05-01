#!/bin/bash
tau=3.18
N=500
for w in 0.1 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4 2.6 2.8 3.0
do
jobname=anderson_w-$w-tau-$tau-N-$N
cd /home/clustor2/ma/g/gl1122/anderson/Dumps
qsub q.sh -v w=$w,tau=$tau,N=$N -N $jobname
done
