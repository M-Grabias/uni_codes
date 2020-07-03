from __future__ import division
import numpy
import random
import matplotlib.pyplot as pyplot
import matplotlib.colors

USER = "Maciej Grabias"
USER_ID = "njgh39"

k = 0.2 # sensitivity
V = 2 # microns per second
Time = 100 #seconds
N_time = 1000 # number of timesteps
r0 = numpy.array( (20.0, 40.0) ) # microns
N_bacteria = 20 # number of bacteria

dt = Time/N_time

def f(x,y):
    return 4000 - (x**2 + y**2)

def speed(v,angle):
    vx = v * numpy.cos(angle)
    vy = v * numpy.sin(angle)
    return numpy.array((vx, vy))

def trajectory(v, n_time, r0):
    history = numpy.zeros((n_time,2))
    shift = [f(r0)]*10
    r = r0 # the starting point and angle
    angle = numpy.pi/6 # for each bacteria beginning to move
    for i in range(n_time):
        history[i] = r
        eNew = f(r)
        shift.append(eNew)
        shift = shift[-10:]
        de = shift[-1] - shift[0]
        t_half = 1 + k * de
        if t_half < 0.1:
            t_half = 0.1
        TAU = t_half/numpy.log(2)
        prob = 1 - numpy.exp(-dt/TAU)
        if random.random() <= prob:
            angle = random.random()*2*numpy.pi
        else:
            r = r + speed(v,angle) * dt
    return history

N_points = 1000
x0,x1 = -40, 80
y0,y1= -20, 50
dx = (x1-x0)/N_points
dy=(y1-y0)/N_points
x_axis = numpy.arange(x0, x1, dx)
y_axis = numpy.arange(y0, y1, dy)
dat = numpy.zeros((len(y_axis), len(x_axis)))
for ix, x in enumerate(x_axis):
    for iy, y in enumerate(y_axis):
        dat[ix, iy] = f(x,y)

msd = numpy.zeros((N_time,1))
msd0 = numpy.zeros((N_time,1))
end = numpy.zeros((N_bacteria,2))

pyplot.figure()

pyplot.subplot(221)

im = pyplot.imshow(numpy.transpose(dat),  extent=(x0, x1, y0, y1),
origin='lower', cmap = matplotlib.cm.gray)

for bacteria in range(N_bacteria):
    route = trajectory(V, N_time, r0)
    pyplot.plot(route[:,0], route[:,-1])
    end[bacteria]=route[-1,:]
    for i in range(N_time):
        msd[i] = msd[i]+(numpy.sqrt((route[i,0]-20)**2 + (route[i,1]-40)**2))**2
        msd0[i] =msd0[i]+(numpy.sqrt((route[i,0]-0)**2 + (route[i,1]-0)**2))**2

msd = msd/20 #get average
msd0 = msd0/20 #get average
pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title("Energy field with 20 \n Bacteria Tracks Overlaid")

pyplot.subplot(222)

for bacteria in range(N_bacteria):
    pyplot.plot([20, end[bacteria,0]], [40, end[bacteria,1]], marker='o')

pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title("Simplified Trajectories \n of 20 Bacteria \n (Initial & Final Position)")

pyplot.subplot(212)

pyplot.plot(numpy.arange(0,100,0.1), msd, label='MSD from the \n initial position')
pyplot.plot(numpy.arange(0,100,0.1), msd0, label='MSD from the \n maximum energy location')

pyplot.xlabel('Time,s')
pyplot.ylabel('Distance, $\mu$m')
pyplot.title("Mean Square Distance against Time")
pyplot.legend(loc="lower right")

pyplot.show()

ANSWER1 = '''Small values of sensitivity, k, result in the bulk bacteria
not to head to the position of maximum energy (as would be expected) but they
rather spread out in random directions. Big values of k don't seem to have much
of an impact on the bulk behaviour.'''
