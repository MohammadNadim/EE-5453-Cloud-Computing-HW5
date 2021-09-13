# modification of passRandomDraw.py
# part2

import numpy
import sys
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n = int(sys.argv[1])
randomVector = numpy.zeros((n,1))

if rank == 0:
  comm.Recv(randomVector, source=ANY_SOURCE, tag=11)
  print "This is the ",n,"x 1 vector."
  print (randomVector)
else:
  randomVector = numpy.random.rand(n,1)
  comm.Send(randomVector, dest=0, tag=11)