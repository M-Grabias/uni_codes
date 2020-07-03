from __future__ import division
import numpy
import random
import matplotlib.pyplot as pyplot
import scipy.integrate

USER = "Maciej Grabias"
USER_ID = "njgh39"

t_half_rad = 20.8 # Half life of 225Ra (days)
t_half_act = 10.0 # Half life of 225Ac (days)
N0 = 250 # Initial number of 225Ra atoms
t1 = 100 # End time for simulation (days)
n_time = 50 # Number of timepoints to solve to

# define analytic function
def analytic(N0, timebase):
    TAU = t_half_rad/numpy.log(2)
    n_atoms = N0 * numpy.exp(-timebase / TAU)
    return n_atoms

# define function using Monte Carlo method
def simulate_monte_carlo(N0, t1, n_time):
    dt = t1/n_time
    count_rad = numpy.zeros(n_time)
    count_act = numpy.zeros(n_time)
    atoms = numpy.ones(250)
    # probabilities of decay within a timestep:
    p_decay_rad = (numpy.log(2) / t_half_rad) * dt
    p_decay_act = (numpy.log(2) / t_half_act) * dt
    for idx_time in range(n_time):
        count_rad[idx_time] = (atoms == 1).sum() # number of undecayed atoms
        count_act[idx_time] = (atoms == 2).sum() # nunmber of atoms that decayed once
        for idx_atom in range(N0):
            if atoms[idx_atom] == 1: #check if it's Ra
                if numpy.random.uniform() <= p_decay_rad:
                    atoms[idx_atom] = 2
            if atoms[idx_atom] == 2:
                if numpy.random.uniform() <= p_decay_act:
                    atoms[idx_atom] = 3
    return (count_rad, count_act)

# define integrating function using Odeint
def f((N_rad, N_act,), t):
    d_n_rad = -(numpy.log(2) / t_half_rad) * N_rad
    d_n_act = -(numpy.log(2) / t_half_act) * N_act - d_n_rad
    return numpy.array((d_n_rad, d_n_act))

# set initial conditions
initial_conditions = (N0, 0)
# timebase to work on
timebase = numpy.arange(0, t1, t1/n_time)

# define values of y to plot on graphs
n_analytic = analytic(N0, timebase)
n_rad = simulate_monte_carlo(N0, t1, n_time)[0]
n_act = simulate_monte_carlo(N0, t1, n_time)[1]
n_odeint_rad = scipy.integrate.odeint(f, initial_conditions, timebase)[:, 0]
n_odeint_act = scipy.integrate.odeint(f, initial_conditions, timebase)[:, 1]

# plot
pyplot.figure()
# analytic graph
pyplot.plot(timebase, n_analytic, color = 'yellowgreen', label = 'Analytic, Radium')
pyplot.xlabel("Time, days")
pyplot.ylabel("Number of atoms")
pyplot.title("Number of Radium and Actinium atoms after radioactive \n decays determined using various methods")
# monte carlo graph
pyplot.plot(timebase, n_rad, color = 'red', label = "Monte Carlo, Radium")
pyplot.plot(timebase,n_act, color = 'blue', label = 'Monte Carlo, Actinium')
# odeint graph
pyplot.plot(timebase, n_odeint_rad, color = 'black', linestyle = '--', label = 'Odeint, Radium')
pyplot.plot(timebase, n_odeint_act, color = 'orange', label = "Odeint, Actinium" )
pyplot.legend()
pyplot.show()
