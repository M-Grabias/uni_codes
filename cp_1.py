import matplotlib.pyplot as ppl
import numpy as np

USER = "Maciej Grabias"
USER_ID = "njgh39"

def f(x):
    return np.cos(x) # function returning a cosine of given input

def g(x):
    return -np.sin(x) # function returning an analytical derivative of the cosine function from above

def g_bdm(x, dx):
    return (f(x) - f(x - dx))/(dx) # function returning a derivative of the cosine function using 
    # backwards difference method

# Series of 100 uniformly spaced values between - 2 pi and 2 pi
xs = np.linspace(-2*np.pi, 2*np.pi, 100)

# Well chosen step dx
gooddx = g_bdm(xs, 7e-8)

# Too big step dx
bigdx = g_bdm(xs, 1e-6)

# Too small step dx
smalldx = g_bdm(xs, 2e-10)

# Error in the analytical and BFM derivative
err1 = gooddx - g(xs)
err2 = bigdx - g(xs)
err3 = smalldx - g(xs)

# Plotted errors
ppl.figure(figsize=(8,4))
ppl.plot(xs, err1, label = 'Well chosen dx')
ppl.plot(xs, err2, label = 'Too big dx')
ppl.plot(xs, err3, label = 'Too small dx')
ppl.xlabel('x')
ppl.ylabel('Error')
ppl.title('Error between analytically and BFM determined derivative of f = cos(x)')
ppl.legend()
ppl.show()

ANSWER1 = "Honestly, I have no idea how to answer that question. Not yet at least."







