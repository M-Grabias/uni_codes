from __future__ import division
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.colors

USER = "Maciej Grabias"
USER_ID = "njgh39"

# starting points, x&y ranges and different gammas:
x00 = 0.3
y00 = 1.0
r0 = numpy.array((x00,y00))
gammas = numpy.array((0.004, 0.001, 0.0001, 0.00001, 0.000001))
x0, x1 = -0.2, 1.2
y0, y1 = -0.2, 1.2

N_points = 1000
dx = (x1-x0)/N_points
dy= (y1-y0)/N_points

N_iterations = 100000

# define functions
def f(x,y):
    return (1-x)**2 + 100 * (y - x**2)**2

def grad((x,y)):
    df_dx = 2 * (200 * x**3 - 200 * x * y + x - 1)
    df_dy = 200 * (y - x**2)
    grad = numpy.array((df_dx, df_dy))
    return grad

def grad_descent((x, y), gamma):
    r = numpy.array((x,y))
    trajectory = numpy.zeros((N_iterations,2))
    for i in range(N_iterations):
        trajectory[i] = r
        r = r - gamma * grad(r)
    return trajectory

# ranges for graph
x_axis = numpy.arange(x0, x1, dx)
y_axis = numpy.arange(y0, y1, dy)

dat = numpy.zeros((len(y_axis), len(x_axis)))

for ix, x in enumerate(x_axis):
    for iy, y in enumerate(y_axis):
        dat[ix, iy] = f(x,y)

pyplot.figure()
im = pyplot.imshow( numpy.transpose(dat),  extent=(x0, x1, y0, y1),
                    origin='lower',
                    cmap = matplotlib.cm.gray,
                    norm=matplotlib.colors.LogNorm(vmin=0.01, vmax=200))

colours = ['blue', 'red', 'green', 'yellow', 'orange']
labels = ['$\gamma = 0.004$', '$\gamma = 0.001$', '$\gamma = 0.0001$',
            '$\gamma = 0.00001$', '$\gamma = 0.000001$']
value = numpy.zeros((5,2))
z=0
for gamma in gammas:
    path = grad_descent(r0, gamma)
    pyplot.plot(path[:,0], path[:,1], color=colours[z], label=labels[z])
    value[z,:] = path[-1]
    z = z+1
xmin, ymin = value[1,0], value[1,1]

pyplot.legend(loc = 'lower left')
pyplot.title("GD Method for Determining the Minima of Rosenbrock's \n"
            "Banana Function for Various Step Sizes $\gamma$")
pyplot.xlim(-0.2, 1.2)
pyplot.ylim(-0.2, 1.2)
pyplot.xlabel("x")
pyplot.ylabel('y')
pyplot.colorbar(im, orientation="vertical",
                label ="$f(x,y)$")
pyplot.show()

ANSWER1 = """ When the step size parameter, gamma, is too big, say of 4x10^-3,
GD method doesn't work as the 'downhill' line converges in some 'odd' place
in a rather hectic manner (blue line on the graph). The appropriate value of
gamma that should be used is of about 10^-3 (red line on the graph) - the
'downhill' line converges at (1.0, 1.0) as expected. For smaller gammas,
ie. <= 10^-4 the 'downhill' line does not precisely converge to the desired
(1.0, 1.0) (green, yellow and orange lines on the graph) for the number
of iterations used (I chose that number to be of N = 100,000). """

ANSWER2 = 'Minima occurs at %.2f, %.2f' % (xmin, ymin)
