from __future__ import division
import numpy
import matplotlib.pyplot as pyplot

USER = 'Maciej Grabias'
USER_ID = 'njgh39'

# constants used
T_HALF = 20.8 #half-time
TAU = T_HALF / numpy.log(2) # average lifetime


def f(n):
    return -n / TAU

def analytic(N0, ts):
    return N0 * numpy.exp(-ts / TAU)

def solve_euler(N0, dt, n_panels):

    #initial parameters
    n, t = N0, 0

    # array for iteration
    n_t = numpy.zeros((n_panels,))

    for i in range(n_panels):
        n_t[i] = n
        t = i * dt
        n = n + f(n) * dt
    return n_t


def solve_heun(N0, dt, n_panels):

    # initial parameters
    n, t = N0, 0

    # array for iteration
    n_t = numpy.zeros((n_panels,))

    for i in range(n_panels):
        n_t[i] = n
        k0 = f(n)
        k1 = f(n + k0 * dt)
        n = n + (k0 + k1) * dt /2
    return n_t


# constants for plots
T1 = 60 # time range
N_PANELS = 15 # number of panels
N0 = 1500 # initial numbe of nuclei


dt = T1 / N_PANELS
ts = numpy.arange(0, T1, dt)

# functions for plots

n_analytic  = analytic(N0, ts)
n_euler     = solve_euler(N0, dt, N_PANELS)
n_heun      = solve_heun(N0, dt, N_PANELS)


#plot

pyplot.figure()
pyplot.subplot(211) # count VS time for methods
pyplot.plot(ts, n_euler, label='Euler Method', color ='red')
pyplot.plot(ts, n_heun, label='Heun Method', color = 'blue', linestyle = '--')
pyplot.plot(ts, n_analytic, label='Analytic', color = 'grey')
pyplot.xlabel("Time, h")
pyplot.ylabel("Number of nuclei")
pyplot.title("Number of nuclei for different methods used VS time")
pyplot.legend()


pyplot.subplot(212) # error VS time for numerics
pyplot.semilogy()
err_euler = abs(n_euler - n_analytic) / n_analytic
err_heun = abs(n_heun - n_analytic) / n_analytic
pyplot.plot(ts, err_euler, color="red", label =" Euler")
pyplot.plot(ts, err_heun, color ="blue", linestyle="--", label="Heun")
pyplot.xlabel("Time, h")
pyplot.ylabel("Error")
pyplot.title("Error between methods used and the analytically determined solution")
pyplot.legend()

pyplot.show()

ANSWER1 = """Heun's method is more accurate than Euler's method because it integrates a differential
equation over trapeziums rather than rectangles"""