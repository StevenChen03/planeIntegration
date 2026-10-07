## This file will consolidate all exercises from Chapter 5
## of Computational Physics into this program.
## This section here is for Python Implementation.

## Importations:
import numpy as np
import time
import numpy as np
from scipy.special import roots_legendre


## Exercise 1: Convert the following pseudocode into three separate functions to perform the rectangular rule integration,
## one to evaluate the function on the left had side of the box, one to evaluate the function on the right
## hand side, and one to evaluate the function in the center of the box. Test your code with the function
## in equation (5.5) in the range 0 to 4 with dx = 0.1. The result should be 4.0. Reduce the box width
## by a factor of 10 (dx = 0.01) and rerun your code noting the result. Continue to reduce the width
## by a factor of 10 each time until you get to 1 × 10−6. Do the results always improve? About what
## decimal place are your answers accurate to as you change the step size? When does the code get
## noticeably slower? How many function evaluations take place for the different step sizes?

## Equation (5.5): f(x) = (x - 2)**3 - 3.5*x + 8

## The pseudocode:
## function rectangularQuad(f, a, b, dx):
## N = (b - a)/dx
## for 0 < i < N:
## x = a + dx/2 + i*dx (for center)
## x = a + (i + 1)*dx (for right)
## x = a + i*dx (for left, also run to N + 1)
## result += f(x)*dx
## return result

def f(x):
    return (x - 2.0)**3 - 3.5* x + 8.0

def left_rectangular_quad(f, a, b, dx):
    N = int(round((b - a) / dx))
    result = 0.0
    for i in range(N):
        x = a + i * dx
        result += f(x) * dx
    return result

def right_rectangular_quad(f, a, b, dx):
    N = int(round((b - a) / dx))
    result = 0.0
    for i in range(N):
        x = a + (i + 1) * dx
        result += f(x) * dx
    return result

def center_rectangular_quad(f, a, b, dx):
    N = int(round((b - a) / dx))
    result = 0.0
    for i in range(N):
        x = a + dx / 2 + i * dx
        result += f(x) * dx
    return result

# Testing the code across different step sizes
dx_values = [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
a, b = 0.0, 4.0

print(f"{'dx':<10} | {'Left Rule':<12} | {'Right Rule':<12} | {'Center Rule':<12}")
print("-" * 55)
for dx in dx_values:
    res_l = left_rectangular_quad(f, a, b, dx)
    res_r = right_rectangular_quad(f, a, b, dx)
    res_c = center_rectangular_quad(f, a, b, dx)
    print(f"{dx:<10} | {res_l:<12.7f} | {res_r:<12.7f} | {res_c:<12.7f}")

## Do the results always improve? 
## THe results for each ule seems to match closer and closer to the 4.0 value,
## I would say that with each lower time step size, the results improve.

## About what decimal place are your answers accurate to as you change the step size?
## The most accurate decimal places with the most accurate results seems to be in the 1e-06
## range at the end of the chart.

## When does the code get noticeably slower?
## The code gets noticeably slower the moment it executes this command where it
## evaluates each function at different time steps as it takes a few seconds to do
## just that and a few more seconds for the rest of the program to resume.

## How many function evaluations take place for the different step sizes?
## Assuming that each time step represents the portion of time in a single second, for each
## decreasing time step value, they take 10 evaluations for 0.1, then 100 evaluations for 0.01, 
## then 1000 evaluations for for 0.001, then 10000 evaluations for for 0.0001, 
## then 100000 evaluations for 1e-5, and finally 1 million evaluations for 1e-5.

print("\n")
print("\n")

## Exercise 2: Add the following function to your available integration functions and perform the same 
## tests as in the previous exercise. Is this method more accurate or a similar level of accuracy to 
## other methods? Is that what you expect? Is there a point that the result becomes less accurate? Why might that be?

def trapezoidalQuad(f, a, b, dx):
    N = int((b-a)/dx) + 1
    w = np.full(N, 1.0)
    w[0] = w[N - 1] = 0.5
    x = np.linspace(a, b, len(w)) ## Ensures that w and x have same length
    dx = x[1] - x[0] ## Handles rounding weirdness
    y = w*f(x)
    return np.sum(y)*dx ## Multiply here to avoid subtractive cancellation

print("Trapezoidal rule results at dx = 0.1:")
print(f"{trapezoidalQuad(f, 0.0, 4.0, 0.1):.1f}")

## The results should come up to 4.0.

print("Trapezoidal rule results at dx = 1e-6:")
print(f"{trapezoidalQuad(f, 0.0, 4.0, 1e-6):.1f}")

## The results should come up to 4.0 (again).

## Is this method more accurate or a similar level of accuracy to other methods?
## This method seems to be a similar level of accuracy to the other methods.

## Is that what you expect?
## The results are as I expected to be.

## Is there a point that the result becomes less accurate?
## It becomes less accurate at larger time steps.

## Why might that be?
## Each time step size represent an evaluation amount per second. With a larger time
## step size, fewer evaluations are made and thus producing less accurate results.
## But with smaller time step sizes, more evaluations are made and thus producing
## more accurate results.


print("\n")
print("\n")

## Exercise 3: Try to compile and run the following code (ask your instructor for help if you run into compiler errors).
## Compare the results of this code with those of the equivalent Python code. Do the results agree?
## One reason they might be different is the optimizations applied by the compiler. Sometimes these
## can lead to different rounding in the least significant digits of the result. Try to time the Python code
## and the C++ code for dx = 1 × 10−6
## Compare the two times to see which version is faster. This is
## the big advantage that C++ has over Python, speed. So, if you ever find yourself with some Python
## code that is just too slow, you may try to translate it into C++.

def trapezoidalQuad_2(f, a, b, dx):
    N = int((b - a) / dx) + 1
    w = [1.0] * N
    w[0] = w[-1] = 0.5
    
    result = 0.0
    dx_adjusted = (b - a) / float(N)
    
    for i in range(N):
        x = a + i * dx_adjusted
        result += w[i] * f(x)
        
    return result * dx_adjusted

if __name__ == "__main__":
    # 1. Test standard run matching C++ main
    print("Trapezoidal rule results in Python Implementation at dx = 0.1:")
    print(f"{trapezoidalQuad_2(f, 0.0, 4.0, 0.1):.15f}")
    
    # 2. Benchmark execution with dx = 1e-6
    print("\nTiming execution for dx = 1e-6...")
    start_time = time.perf_counter()
    res = trapezoidalQuad_2(f, 0.0, 4.0, 1e-6)
    end_time = time.perf_counter()
    
    print(f"Trapezoidal rule results in Python Implementation at dx = 1e-6: {res:.15f}")
    print(f"Python Execution Time: {end_time - start_time:.6f} seconds")

## The standard Trapezoidal rule results should come up to 3.842589659918160.
## The dx should equal 1e-6, giving the results as 3.999998000005220.
## It should take 0.519603 seconds to execute this portion of the command.

## Which is faster?
## Between the two, the C++ version is faster.

print("\n")
print("\n")

## Exercise 4: Add this function to your growing list of ways to compute the numerical integral of our test function.
## Run through the same tests that we did before, looking at the behavior as a function of the step size. 

def simpsonsQuad(f, a, b, dx):
    N = int((b-a)/dx) + 1
    if (N % 2 == 0): N += 1 # Check if N is even, make odd if needed
    w = np.zeros(N) # Array of N elements, all set to zero
    # Use array slicing to set the values of our weight array
    w[::2] = 2.0
    w[1::2] = 4.0
    w[0] = w[N-1] = 1.0 # Set first and last values
    x = np.linspace(a, b, len(w)) # Compute evaluation points
    dx = x[1] - x[0] # Compute spacing since might be different
    y = w*f(x)/3.0
    return np.sum(y)*dx

print("Simpson's rule results in Python Implementation at dx = 0.1:")
print(f"{simpsonsQuad(f, 0.0, 4.0, 0.1):.15f}")
print("Simpson's rule results in Python Implementation at dx = 1e-6:")
print(f"{simpsonsQuad(f, 0.0, 4.0, 1e-6):.15f}")

## The Simpson's rule results should give 4.000000000000000.
## At dx = 1e-6, The Simpson's rule results should give 3.999999999999999.

print("\n")
print("\n")

## Exercise 6: Let’s now do a more detailed examination of our algorithms. Start with dx = 0.7 and look at the
## result of integrating our test function with all of the different methods discussed so far. Which is the
## most accurate at this point? Individually adjust dx for each of the methods until you reach the same
## level of accuracy as the most accurate method from the first run. Once you have these different 푑푥
## values, use them to estimate the number of function evaluations used for each method. You should
## see that the most accurate method with our initial dx will have the fewest function evaluations,
## making it the best choice (so far). Not only does fewer function evaluations means less round-off
## error, it also means a faster program since most of the time when we resort to numerical integration,
## our function will be computationally taxing to compute, otherwise we probably would have just
## done it by hand.

## All calculations with dx = 0.7
print("Trapezoidal rule results at dx = 0.7:")
print(f"{trapezoidalQuad(f, 0.0, 4.0, 0.7):.15f}")
print("\n")
print("Trapezoidal rule results in Python Implementation at dx = 0.7:")
print(f"{trapezoidalQuad_2(f, 0.0, 4.0, 0.7):.15f}")
print("\n")
print("Simpson's rule results in Python Implementation at dx = 0.7:")
print(f"{simpsonsQuad(f, 0.0, 4.0, 0.7):.15f}")
print("\n")

## The default Trapezoidal rule results at dx = 0.7 should give 3.999999999999998.
## The modified Trapezoidal rule results in Python Implementation at dx = 0.7 should give 3.765432098765432
## The Simpson's rule results in Python Implementation at dx = 0.7: 3.9999999999999994.

## Turns out, the provided dx value of 0.7 from the book is the value that gives the closest results with one another.
## Trying any other value seems to shift the value of the results up or down.

print("\n")
print("\n")

## Exercise 7: Add the following function to your growing library of Python functions to compute numerical integrals.
## Use it to integrate our test function with n = 2. Also try it for n = 3. Is there any benefit to adding
## another function evaluation with the Gaussian quadrature method?

def gaussianQuad(f, a, b, n):
    x, w = roots_legendre(n)
    y = w*f(((b-a)/2.0)*x + (b+a)/2.0)
    return np.sum(y)*(b-a)/2.0

print("Gaussian Quadrature results in Python Implementation at n = 2:")
print(f"{gaussianQuad(f, 0.0, 4.0, 2):.15f}")
print("Gaussian Quadratureresults in Python Implementation at n = 3:")
print(f"{gaussianQuad(f, 0.0, 4.0, 3):.15f}")

## At n = 2, The Gaussian Quadrature results should give 4.000000000000002.
## At n = 3, The Gaussian Quadrature results should give 3.999999999999998.

## Is there any benefit to adding another function evaluation with the Gaussian quadrature method?
## The benefit here is that with another function added, more variations of the results are 
## presented and that gives us more opportunities to compare them.

## Thoughts: Between Python and C++, I honestly think that C++ is more accurate in this situation
## because its results seem to match up better. But that's just my opinion. For now, I'll stick
## to using Python for my calculations since I'm more familiar with it, but will touch upon C++
## in the future.