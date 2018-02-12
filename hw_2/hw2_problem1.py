# -*- coding: utf-8 -*-
"""
Spyder Editor
Nick Cinko
AY250 HW2 Problem 1
Goal: Reproduce one of your old published-paper quality plots with Bokeh. 

Original file is Mn2alphadetrended.png.  The data is hourly counts from a Mn-54 source over a ~200 day period.  
It is detrended using the decay constant, lambda, and scaled to 1 (first data point is pinned to 1).  If the data 
were perfectly exponential, this would produce a horizontal line.  Further detrending is done with an "alpha" parameter, 
to minimize a residual "U-shape" distortion in the data (mainly due to the way detector dead-time between counts is handled).  
With this detrending scheme, the two parameters (alpha, lambda) are strongly coupled in a source with a relatively short half-life
(< 1 year).  I added interactive sliders to the plot so the user can adjust the parameters away from their best-fit values
and see the immediate effect on the detrended data.  I think it helps build some intuition for the interplay between the two 
parameters and the meaning of each value's precision.  For example, you could adjust lambda by a few multiples of the quoted 
statistical error and see how it affects the plot.
"""

import numpy as np
from bokeh.layouts import column, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource

#read in data file
data = np.load('data/data.npz')
times = data['T']
counts = data['ROI']
sumcounts = data['Sum']

#exponentially detrend data
default_lambda = 2.221
default_alpha = 3.8
detrend = counts*np.exp(times*default_lambda/1e3 - default_alpha*sumcounts/1e10)/(counts[0]*np.exp(-default_alpha*sumcounts[0]/1e10))

#make scatter plot
source = ColumnDataSource(data=dict(x=times, y=detrend, ytemp=counts, ysum=sumcounts))
plot = figure(y_range=(0.998, 1.001), plot_width=1200, plot_height=600, title ='Mn-54 834.8 keV peak')
plot.title.align = 'center'
plot.xaxis.axis_label = 'time (days)'
plot.yaxis.axis_label = 'detrended counts (hourly)'
plot.scatter('x', 'y', source=source, size = 2)

#add fitting interactivity
callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var lam = lambda.value;
    var alpha = alpha.value
    x = data['x']
    y = data['y']
    y2 = data['ytemp']
    ysum = data['ysum']
    for (i = 0; i < x.length; i++) {
        y[i] = y2[i]*Math.pow(2.71828, lam*x[i]/1e3-alpha*ysum[i]/1e10)/(y2[0]*Math.pow(2.71828,-alpha*ysum[0]/1e10))
    }
    source.change.emit();
""")

lambda_slider = Slider(start=2.10, end=2.40, value=default_lambda, step=0.001,
                    title="lambda (E-3)", callback=callback)
callback.args["lambda"] = lambda_slider

alpha_slider = Slider(start=0, end=10, value=default_alpha, step=0.01,
                    title="alpha (E-10)", callback=callback)
callback.args["alpha"] = alpha_slider

layout = column(
    plot,
    widgetbox(lambda_slider),
    widgetbox(alpha_slider),
)

output_file("detrend.html", title="Mn-54 detrending")

show(layout)