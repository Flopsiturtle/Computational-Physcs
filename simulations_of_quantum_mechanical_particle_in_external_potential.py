# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 12:33:12 2024

@author: Florian Hollants
"""
import numpy as np
#declaring variables
H_BAR = 1
MASS = 1
D = 2
N = 5
A = 1
OMEGA=1
R=1
T=1
M=100






MU=MASS*OMEGA*R**2/H_BAR
EPSILON = A/R
TAU=OMEGA*T/M




shape = (N,)  # tuple of D N's to shape ndarrays correctly
origin = (0,)  # tuple of D zeros to call position in grid later
for _ in range(D-1):
    shape += (N,)
    origin += (0,)

Psi=np.arange(N**D).reshape(shape).astype('complex')

V=np.empty_like(Psi)
for n, _ in np.ndenumerate(Psi):
    V[n]=np.dot(np.array(n)-int(N/2),np.array(n)-int(N/2))


def laplace(func):
    """calculating the laplacian of ndarray"""
    lap = -2*D*func
    for j in range(D):
        lap += (np.roll(func, -1, axis=j)
                +np.roll(func, 1, axis=j))
    return lap/A**2


def hamilton(func):
    """calculating the hamiltonian for double harmonic well"""
    return -1/(2*MU*EPSILON**2)*laplace(func)+MU/8*(EPSILON**2*V-1)**2

def time_evol(func):
    """time evolution using second-order Fourier transform"""
    for _ in range(M):
        func = func - 1j*hamilton(func)*TAU-TAU**2*hamilton(hamilton(func))/2
    return func

print(laplace(Psi))
print(hamilton(Psi))
print(time_evol(Psi))