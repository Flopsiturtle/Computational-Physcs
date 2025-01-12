import numpy as np

import variables
import hamiltonian


""" --- conjugate gradient --- """
# A x = b
# H x = v -> x = H^-1 v     # so conjugate gradient gives x as result which is our wanted quantity
# now: implement hamiltonian in function itself

def Hinv(v,tolerance,maxiters,mu,epsilon):
    size = (v.shape)[0]
    D = len(v.shape)    
    x0 = np.zeros((size,)*D)   
    r0 = v - hamiltonian.hamilton_variable(x0,mu,epsilon)
    if np.max(r0) <= tolerance:    
        return x0
    p0 = r0
    for i in np.arange(1,maxiters+1):
        alpha0 = (np.vdot(r0,r0)) / (np.vdot(p0,hamiltonian.hamilton_variable(p0,mu,epsilon)))    
        x = x0 + alpha0*p0
        r = r0 - alpha0*hamiltonian.hamilton_variable(p0,mu,epsilon)
        if np.max(r) <= tolerance: 
            return x
        if i == maxiters:
            return 'Error1'    
        beta = (np.vdot(r,r)) / (np.vdot(r0,r0))
        p0 = r + beta*p0
        x0 = x
        r0 = r



''' --- Arnoldi method --- '''

def norm(vector):
    return np.sqrt(np.vdot(vector,vector))

def matrix_multi(vector, iterations, error_Hinv, maxiters_Hinv,mu,epsilon):
    for i in range(iterations):
        w = Hinv(vector, error_Hinv, maxiters_Hinv,mu,epsilon)
        vector = w
    return vector

def gram_schmidt(array):
    space = []
    for i in range(len(array)):
        w = array[i]
        a = w
        for j in range(len(space)):
            a += -np.vdot(space[j], w)*space[j]
        a = a/norm(a)
        space.append(a)
    return space
        
def krylov_space(vector, number_eigen, error_Hinv, maxiters_Hinv,mu,epsilon):
    space = []
    for i in range(number_eigen):
        space.append(matrix_multi(vector, i, error_Hinv, maxiters_Hinv,mu,epsilon))
    return space 

def matrix_once(array, error_Hinv, maxiters_Hinv,mu,epsilon):
    space = []
    for i in range(len(array)):
        space.append(matrix_multi(array[i], 1, error_Hinv, maxiters_Hinv,mu,epsilon))
    return space 

def eigenvalues(array, error_Hinv, maxiters_Hinv,mu,epsilon):
    space = []
    for i in range(len(array)):
        w = array[i]
        eigen = np.vdot(w, matrix_multi(w, 1, error_Hinv, maxiters_Hinv,mu,epsilon))
        space.append(eigen)
    return space

def arnoldi(v, number_eigen, error_arnoldi, maxiter_arnoldi, error_Hinv, maxiters_Hinv,mu,epsilon):
    vectors = krylov_space(v, number_eigen, error_Hinv, maxiters_Hinv,mu,epsilon)
    for count, j in enumerate(range(maxiter_arnoldi)):
        errors = []
        vectors = matrix_once(vectors, error_Hinv, maxiters_Hinv,mu,epsilon)
        orth_vectors = gram_schmidt(vectors)
        eigen = eigenvalues(orth_vectors, error_Hinv, maxiters_Hinv,mu,epsilon)
        for i in range(len(vectors)):
            LHS = matrix_multi(orth_vectors[i], 1, error_Hinv, maxiters_Hinv,mu,epsilon)
            RHS = eigen[i]*orth_vectors[i]
            error = norm(LHS - RHS)
            errors.append(error)
        if np.all(np.array(errors)) <  error_arnoldi:
            return 1/np.array(eigen),orth_vectors
        else:                     
            vectors = orth_vectors
            #print(np.max(errors))
        if j == maxiter_arnoldi-1:
            print('!!maxiter reached in Arnoldi!!')
            return 'Error2','Error2'
