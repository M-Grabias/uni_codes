from __future__ import division
import numpy
import scipy.integrate
import matplotlib.pyplot as pyplot

USER = 'Maciej Grabias'
USER_ID = 'njgh39'

r = 0.15 # radius of the cannonball in meters
rho_iron =  7874.00 # density of iron in kg m-3
g =  9.81 # acceleration due to gravity in ms-2
kappa =  0.47 # drag coefficient of a sphere
rho_air =  1.23 # density of air in kg m-3
t1 =  25.00 # end time for our ODE integration in s
v0 = 125.00 # launch speed in m s-1
n_panels =  400 # the number of panels to use

# cross section area & mass of cannonball determined using above

area = numpy.pi* r**2
mass = rho_iron * (4/3) * numpy.pi * r**3

# define the function
def f((x, y, vx, vy),t):

    # gravitational forces
    Fx_grav = 0
    Fy_grav = - mass * g

    # drag forces
    Fx_drag = - kappa * rho_air * area * v0 * vx
    Fy_drag = - kappa * rho_air * area * v0 * vy


    d_x = vx # dx/dt
    d_y = vy # dy/dt
    d_vx =  Fx_drag / mass # dvx/dt
    d_vy = (Fy_drag + Fy_grav) / mass # dvy/dt

    return numpy.array((d_x, d_y, d_vx, d_vy))


def solve_euler(state, t1, n_panel):

    history = numpy.zeros((n_panels, len(state)))
    dt = t1 / n_panels

    # integrate with Euler method
    for i in range(n_panels):
        history[i] = state
        state = state + f(state, dt * i) * dt
    return history

# define timebase
timebase = numpy.arange(0, t1, t1 / n_panels)

def trim_trajectory(values):

    # process trajectory to terminate when below y = 0
    for i in range(len(values) - 1):
        x0, y0, vx0, vy0 = values[i]
        x1, y1, vx1, vy1 = values[i + 1]
        if y0 < 0: return values[:i]
    return values

proj_range = []
thetas = range(5,90,5)

pyplot.subplot(211)

for theta in thetas:

    vx, vy = numpy.cos(numpy.deg2rad(theta)) * v0, numpy.sin(numpy.deg2rad(theta)) * v0
    initial_conditions = (0, 0, vx, vy)

    values_scipy = scipy.integrate.odeint(f, initial_conditions, timebase)
    values_euler = solve_euler(initial_conditions, t1, n_panels)
    values_scipy = trim_trajectory(values_scipy)
    values_euler = trim_trajectory(values_euler)

    # calculate range

    x_first, y_first, vx_first, vy_first = values_scipy[0]
    x_final, y_final, vx_final, vy_final = values_scipy[-1]

    rnge = x_final - x_first

    proj_range.append(rnge)

    # trajectory for scipy integrate
    x_scipy = values_scipy[:, 0]
    y_scipy = values_scipy[:, 1]

    # trajectory for Euler integrate
    x_euler = values_euler[:,0]
    y_euler = values_euler[:,1]

    # plot trajectories
    pyplot.plot(x_scipy, y_scipy, color = 'grey', label = "Odeint")
    pyplot.plot(x_euler, y_euler, color = 'blue', linestyle = '--', label = "Euler")
    pyplot.title("Trajectories for Euler & Odeint Methods")
    pyplot.xlabel("X coordinate")
    pyplot.ylabel("Y coordinate")

pyplot.legend(("Odeint", "Euler"))

# plot range VS launch angle
pyplot.subplot(212)
pyplot.plot(thetas, proj_range, color = 'red')
pyplot.title("Range VS Launch Angle")
pyplot.xlabel("Launch Angle, deg")
pyplot.ylabel("Range, m")

pyplot.show()

ANSWER1 = """ The angle from the horizontal for maximum range under these
conditions is 40 degrees."""
ANSWER2 = """ The angle decreases with increasing air density """
