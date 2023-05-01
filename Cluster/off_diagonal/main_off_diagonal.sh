#!/bin/bash
sd=0.1
tau=0.5
N=1000
jobname=offdiagonal_sd-$sd-tau-$tau-N-$N
cd ${HOME}/off_diagonal
qsub q.sh -v sd=$sd,tau=$tau,N=$N -N $jobname
