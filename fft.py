from cmath import exp, pi
from math import log
import random

from time import time

def Q15(x):
	return [ hex(int(x.real * (1<<15)) & 0xFFFF) , hex(int(x.imag * (1<<15)) & 0xFFFF) ] 
 
def fft_rdx2a(x):
    N = len(x)
    if N <= 1: return x
    even = fft_rdx2a(x[0::2])
    odd =  fft_rdx2a(x[1::2])
    T = [exp(-2j*pi*k/N)*odd[k] for k in range(N/2)]
    #print len(even)+len(odd),[Q15(exp(-2j*pi*k/N)) for k in range(N//2)],N/2
    return [even[k] + T[k] for k in range(N/2)] + \
           [even[k] - T[k] for k in range(N/2)]
           
def fft_rdx4a(x):
	N = len(x)
	if N <=1: return x
	x1 = fft_rdx4a(x[0::4])
	x2 = fft_rdx4a(x[1::4])
	x3 = fft_rdx4a(x[2::4])
	x4 = fft_rdx4a(x[3::4])
	
	t2 = [exp(-2j*pi*k/N)*x2[k] for k in range(N/4)]
	t3 = [exp(-2j*pi*2*k/N)*x3[k] for k in range(N/4)]
	t4 = [exp(-2j*pi*2*k/N)*x4[k] for k in range(N/4)]
	
	return [ (x1[k] + t2[k] + t3[k] + t4[k]) for k in range(N/4) ] + \
		   [ (x1[k] - complex(0,1)*t2[k] - t3[k] + complex(0,1)*t4[k]) for k in range(N/4) ] + \
		   [ (x1[k] - t2[k] + t3[k] - t4[k]) for k in range(N/4) ] + \
		   [ (x1[k] + complex(0,1)*t2[k] - t3[k] - complex(0,1)*t4[k]) for k in range(N/4) ]
	
	#T = [ for k in range(N/2) ]
	
def fft_full(x):
	X = [0 for i in range(len(x)) ]
	N = len(x)
	for k in range(len(X)):
		for n in range(len(x)):
			X[k]+= x[n] * exp(-2j*pi*k*n/N)
	return X

#x = [random.random() for x in range(8)]
#print fft([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0])

x = [x for x in range(4**6)]

ta = time()
Xa = fft_full(x)
ta = time() - ta

tb = time()
Xb = fft_rdx2a(x)
tb = time() - tb

tc = time()
Xc = fft_rdx4a(x)
tc = time() - tc

diff = sum([ (Xa[i] - Xb[i]) for i in range(len(x)) ])
print "diffab:",round(diff.real + diff.imag)
diff = sum([ (Xa[i] - Xc[i]) for i in range(len(x)) ])
print "diffac:",round(diff.real + diff.imag)

print "ta:",ta
print "tb:",tb
print "tc:",tc

