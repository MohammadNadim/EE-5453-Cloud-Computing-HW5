# modification of trapParallel_1.py
# part 4

import numpy
import sys
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

a = float(sys.argv[1])
b = float(sys.argv[2])
n = int(sys.argv[3])

def f(x):
  return x*x

def integrateRange(a, b, n):
  integral = -(f(a) + f(b))/2.0 
  for x in numpy.linspace(a,b,n+1):
    integral = integral + f(x)  
  integral = integral* (b-a)/n
  return integral


h = (b-a)/n

if n%size == 0:
  local_n = n/size
else:
  if ((rank)<(n%size)):
    local_n = math.floor(n/size)+1
    #print rank, local_n
  else:
    local_n = math.floor(n/size)
    #print rank, local_n
  
local_a = a + rank*local_n*h
local_b = local_a + local_n*h
integral = numpy.zeros(1)
total = numpy.zeros(1)
integral[0] = integrateRange(local_a, local_b, local_n)

comm.Reduce(integral, total, op=MPI.SUM, root=0)

if comm.rank == 0:
  print "With n =", n, "trapezoids, our estimate of the integral from", a, "to", b, "is", total