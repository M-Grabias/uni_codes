from __future__ import division 
import numpy
import matplotlib.pyplot as pyplot

USER = "Maciej Grabias"
USER_ID = 'njgh39'

def f(x):
    return (x**2.0)*numpy.sin(x) # function returning product of x squared times sin(x)

def g(x):
    return 2.0*x*numpy.sin(x) - (x**2.0 - 2.0)*numpy.cos(x) # function returning indefinite integral of 
    # function above

def integrate_numeric(x0, x1, n_panels): # function returning the area under the curve of f(x)
    # using Simpson's rule
    panel_width = (x1 - x0) / n_panels
    area = 0.0
    

    for ix in range(n_panels):
        a = x0 + ix * panel_width
        panel_area = (panel_width/6) * (f(a) + 4 * f(a + panel_width/2) + f(a + panel_width))
        area = area + panel_area
    return area

def integrate_analytic(x0, x1):
    return g(x1) - g(x0)


PANEL_COUNTS = [4, 8, 16, 32, 64, 128, 256, 512, 1024]

X0 = 0
X1 = 2

y_data = []
ref = integrate_analytic(X0, X1)

for n in PANEL_COUNTS:
    s = integrate_numeric(X0, X1, n)
    error = abs((s-ref)/ref)
    y_data.append(error)

pyplot.figure(figsize = (6,6))
pyplot.loglog()
pyplot.scatter(PANEL_COUNTS, y_data)
pyplot.ylabel('Percentage Error')
pyplot.xlabel('Number of Panels')
pyplot.title("Percentage Error in the Numerical Method VS Number of Panels Used \n (both scales logarithmic)")
pyplot.show()

ANSWER1 = "The increasing number of panels increases the accuracy of the numerical method because \
narrower panels enable more accurate iteration and summation"
ANSWER2 = "Increasing panel count will still increase the accuracy of the method, but not as much \
as it does while using Simpson's method.'"

