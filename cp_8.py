from __future__ import division
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.colors

USER = "Maciej Grabias"
USER_ID = "njgh39"

def f(z):
    return z**4 -1

def df(z):
    return 4*z**3

def N_R(seed):
    z = seed
    gamma = 10
    iteration = 0
    while gamma > 0.03 and iteration < 50:
        z = z - f(z)/df(z)
        iteration += 1
        gamma = abs(f(z) - 0)
    return z, iteration

def numerate(seed):
    zeros = N_R(seed)
    zero = zeros[0]
    if abs(zero - 1) < 0.01:
        color = 0
    elif abs(zero + 1) < 0.01:
        color = 1
    elif abs(zero + 1j) < 0.01:
        color = 2
    elif abs(zero - 1j) < 0.01:
        color = 3
    else:
        color = 4
    return color

pyplot.figure()
x0, x1 = -2., 2.
y0, y1 = -2., 2.
N_points = 400
dx = (x1-x0)/N_points
dy= (y1-y0)/N_points
x_axis = numpy.arange(x0, x1, dx)
y_axis = numpy.arange(y0, y1, dy)
dat = numpy.zeros((len(y_axis), len(x_axis)))
dat2 = numpy.zeros((len(y_axis), len(x_axis)))
for ix, x in enumerate(x_axis):
    for iy, y in enumerate(y_axis):
        dat[ix, iy] = numerate(complex(x,y))
        dat2[ix, iy] = N_R(complex(x,y))[1]
pyplot.subplot(121)
im = pyplot.imshow(numpy.transpose(dat),
                    extent=(x0, x1, y0, y1),
                    origin='lower',
                    cmap='viridis')
pyplot.xlabel("Real")
pyplot.ylabel("Imaginary")
pyplot.title("Newton-Raphson Method for \n Various Starting Points")
pyplot.subplot(122)
im2 = pyplot.imshow(numpy.transpose(dat2),
                    extent=(x0, x1, y0, y1),
                    origin='lower',
                    cmap='viridis')
pyplot.colorbar(im2, orientation='horizontal', label='Time')
pyplot.xlabel("Real")
pyplot.ylabel("Imaginary")
pyplot.title("Convergence Time")
pyplot.show()

ANSWER1 = ''' The diagrams show the chaotic behaviour of the Newton-Raphson
method as the position of the root, as well as the time it takes to coverge to
to it is highly sensitive the initial input point. The images are said to be
fractal in nature because when zoomed in enough times, a resemblence to the
"original" picture can be found due to endless detail in the generated graphs. '''
