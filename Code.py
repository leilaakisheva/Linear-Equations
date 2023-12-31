###**Methods**###
####**Part I**####

import numpy as np
import random
import timeit
from scipy.linalg import lu_factor, lu_solve
import matplotlib.pyplot as plt

"""First I create 'Gauss' function. The function takes two arguments, A and b, which represent the coefficient matrix and the constant vector, respectively.
The function returns the solution to the system of linear equations Ax=b as a vector x. If the system is inconsistent or has multiple solutions, the function probably will return a valid solution, but not necessarily the unique one.
"""

def Gauss(A, b):
#The number of equations in the system (the same as the length of the vector b)
    N=len(b)
#First, I have to find the index of the row with the largest absolute value in the i-th column of the matrix A (pivot row)
    for i in range(N):
        pivot_col=i
        pivot_val=abs(A[i, i])
        for j in range(i+1, N):
            if abs(A[j, i])>pivot_val:
                pivot_col=j
                pivot_val=abs(A[j, i])
        pivot_row=pivot_col

        #Then I should swap the i-th row with the pivot row in the matrix A and vector b
        #This is done to be sure that the pivot element (the element in the i-th column and i-th row) is nonzero
        if i!=pivot_row:
            A[[i,pivot_row]]=A[[pivot_row,i]]
            b[[i,pivot_row]]=b[[pivot_row,i]]

        #Then I need to compute a factor that is used to subtract a multiple of the i-th row from each subsequent row
        for j in range(i + 1, N): #Eliminating the i-th variable
            factor=A[j, i]/A[i, i]
            A[j, i+1:]=A[j, i+1:]-(A[j, i]/A[i, i])*A[i, i+1:]
            b[j]=b[j]-(A[j, i]/A[i, i])*b[i]
        #The matrix A and vector b have been transformed into an upper-triangular form.
    x=np.zeros(N)
#back-substitution to solve for the variables:
    for i in range(N-1,-1,-1):
        x[i]=(b[i]-np.dot(A[i,i+1:], x[i+1:]))/A[i, i]
#iterating over the rows of the matrix A in reverse order, starting from the last row
    return x

"""For each row, I use the previously computed values of x to compute the value of the current variable, and store this value in the corresponding entry of x
This process continues until all variables have been solved for.

I use slice notation to update the rows of the coefficient matrix in the elimination loop, which makes the code more concise and easier to read. I also use the A[i, i:] slice to avoid copying the same values multiple times, which should improve the performance.

Then I introduce the Gauss_error function to compute the relative error.
I used residual error $r = B - A@x $, which is the difference between the right-hand side vector B and the product of the matrix A with the solution vector x in the calculations. Also, I used the notation of Euclidean norm of the two sets of vectors: $$||e|| =\sqrt{e_1^2+e_2^2+e_3^2+...+e_n^2}$$
Then, I calculate the relative error by dividing the Euclidean norm of the residual vector by the Euclidean norm of the right-hand side vector. The relative error represents the accuracy of the solution x and is usually expressed as a percentage. A small value of rel_error indicates a more accurate solution.
"""

#Computing error using the expected value of the function
def Gauss_error(A,B):
  x = B/np.diag(A)
  r = B-A @ x
  r_norm = np.linalg.norm(r, 2)
  b_norm = np.linalg.norm(B, 2)
  rel_error = r_norm/b_norm
  return rel_error

"""Now, I compute the LU decomposition to get L matrix and U matrix. Then, having these two parts I can solve the system."""

def lu_decomposition(A):
    n = len(A)
    U = np.copy(A)
    L = np.eye(n)
    for k in range(n-1):
        for i in range(k+1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
    return L, U

def solve_lu_decomposition(A, b):
    L, U = lu_decomposition(A)
    n = len(A)
    y = np.zeros(n)
    x = np.zeros(n)
    # Solving Ly = b
    for i in range(n):
        y[i] = b[i]-sum(L[i][j]*y[j] for j in range(i))
    # Solving Ux = y
    for i in range(n-1, -1, -1):
        x[i] = (y[i]-sum(U[i][j]*x[j] for j in range(i+1, n))) / U[i][i]
    return x

def lu_error(A, B):
    L, U = lu_decomposition(A)
    y = np.linalg.solve(L, B)
    x = np.linalg.solve(U, y)
    Ax = np.dot(A, x)
    r = B - Ax
    r_norm = np.linalg.norm(r, 2)
    b_norm = np.linalg.norm(B, 2)
    rel_error = r_norm / b_norm
    return rel_error

"""Now, I test these functions for the random values of k1, k2,F1,F2 in the given interval."""

k1=random.randrange(1,5)
k2=random.randrange(1,5)
f1=random.randrange(2,4)
f2=random.randrange(2,4)
A=np.array([[k1+k2,-k2], [-k2,k2]], dtype=float)
B=np.array([f1,f2], dtype=float)
x_lu=solve_lu_decomposition(A,B)
x_lu_error=lu_error(A,B)
x_gauss_error=Gauss_error(A,B)
x_gauss=Gauss(A,B)

print("Lu decomposition solution: \n", x_lu)
print("Gauss elimination solution: \n", x_gauss)
print("LU decomposition error: ", x_lu_error)
print("Gauss elimination error: ",x_gauss_error )

"""It can be seen that for some reason the Gauss method gives a huge error, although the solutions of the LU method and Gauss elimination method are the same.

###**Part II**###

Now I generate random values for the matrix a and b with the given array size.
Both methods work out well.
"""

N = 5  # size of matrix and vector
#Generating a matrix  N×N , with randomly generated elements
a = np.random.uniform(-10, 10, size=(N, N))
b = np.random.uniform(-5, 5, size=N)
x_lu=solve_lu_decomposition(a,b)
x_lu_error=lu_error(a,b)
x_gauss=Gauss(a,b)
x_gauss_error=Gauss_error(a,b)
print("Lu decomposition solution: \n", x_lu)
print("Gauss elimination solution: \n", x_gauss)
print("LU decomposition error: ", x_lu_error)
print("Gauss elimination error: ",x_gauss_error )

"""I should measure time taken by each method for various N."""

N = 2
i=0
total_time1 = np.zeros(99)
total_time2 = np.zeros(99)

while N<=100:
    a = np.random.uniform(-10, 10, size=(N, N))
    b = np.random.uniform(-5, 5, size=N)

    start_time = timeit.default_timer()
    solve_lu_decomposition(a, b)
    total_time1[i] = timeit.default_timer() - start_time

    start_time = timeit.default_timer()
    Gauss(a, b)
    total_time2[i] = timeit.default_timer() - start_time
    N=N+1
    i=i+1
total_time1 = np.cumsum(total_time1)
total_time2 = np.cumsum(total_time2)

x=np.arange(2,101)
plt.plot(x, total_time1[0:], label="LU decomposition")
plt.plot(x, total_time2[0:], label="Gaussian elimination")
plt.xlabel("N")
plt.ylabel("Time (s)")
plt.legend()
plt.show()

"""###**Results**###
It can be seen that both methods work fine for small linear systems, like in the part I. However, as the size of the matrix increases, the GE method has a better performance. Starting from N=10 there is a difference in execution time.

###**Conclusion**###
It was found that both methods work good for small linear systems ($N<10$), however as the size increases the Gaussian elimination method is preferrable because of compilation time.
"""
