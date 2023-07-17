# Linear-Equations
In this assignment we had to create functions for Gauss Elimination and LU decomposition methods and compare their performance for various N - number of dimensions. It was asked to find the equilibrium positions of two blocks which have different eq. of motions. This task was implemented using Gauss Elimination method and LU decomposition method. 

There were two parts of the assignment. In the 1st parrt it was asked to find the equilibrium positions of two blocks which have different eq. of motions. This task was implemented using Gauss Elimination method and LU decomposition method. Then, we had to compare results and corresponding error values. In the second part we were asked to measure the time taken to compile each method for large number of N and then make a plot.


First I create 'Gauss' function. The function takes two arguments, A and b, which represent the coefficient matrix and the constant vector, respectively. The function returns the solution to the system of linear equations Ax=b as a vector x. If the system is inconsistent or has multiple solutions, the function probably will return a valid solution, but not necessarily the unique one.


For each row, I use the previously computed values of x to compute the value of the current variable, and store this value in the corresponding entry of x This process continues until all variables have been solved for.


I use slice notation to update the rows of the coefficient matrix in the elimination loop, which makes the code more concise and easier to read. I also use the A[i, i:] slice to avoid copying the same values multiple times, which should improve the performance.


Then I introduce the Gauss_error function to compute the relative error. I used residual error  r=B−A@x , which is the difference between the right-hand side vector B and the product of the matrix A with the solution vector x in the calculations. Also, I used the notation of Euclidean norm of the two sets of vectors:


||e||=e21+e22+e23+...+e2n−−−−−−−−−−−−−−−−√ 


Then, I calculate the relative error by dividing the Euclidean norm of the residual vector by the Euclidean norm of the right-hand side vector. The relative error represents the accuracy of the solution x and is usually expressed as a percentage. A small value of rel_error indicates a more accurate solution.


Lu decomposition solution: 
 [1.66666667 3.66666667]
Gauss elimination solution: 
 [1.66666667 3.66666667]
LU decomposition error:  1.2316818592266835e-16
Gauss elimination error:  0.5924200692595909
It can be seen that for some reason the Gauss method gives a huge error, although the solutions of the LU method and Gauss elimination method are the same.



![image](https://github.com/leilaakisheva/Linear-Equations/assets/128895782/2b81e817-045c-49f0-a5ae-6748b0af6312)


Results
It can be seen that both methods work fine for small linear systems, like in the part I. However, as the size of the matrix increases, the GE method has a better performance. Starting from N=10 there is a difference in execution time.


Conclusion
It was found that both methods work good for small linear systems ( N<10 ), however as the size increases the Gaussian elimination method is preferrable because of compilation time.
