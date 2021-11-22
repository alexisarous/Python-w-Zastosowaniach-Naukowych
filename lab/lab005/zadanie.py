from bokeh.core.enums import Orientation, VerticalAlign
from bokeh.plotting import figure, show, row, column
from bokeh.io import curdoc
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap
from bokeh.palettes import all_palettes
from bokeh.layouts import layout
from bokeh.models import Slider

import numpy as np
import scipy.special as sp

time = []
first = []
second = []

width = 15

def generate_data():
    b = np.linspace(0, width, 500)

    v = 1
    bessel1 = sp.jv(v, b/2) * sp.jv(v, b/2)

    v = 2
    bessel2 = sp.jv(v, b/2) * sp.jv(v, b/2)

    data = {'xB': b, 'yB1': bessel1, 'yB2': bessel2}
    return data


def callback(attr, old, new):
    global width
    width = slider.value

    data = generate_data()

    g1.data_source.data = data



f = open('dane.txt', 'r', encoding = 'utf8')

for line in f:
    i = 0
    for words in line.lstrip().split('\n'):
        for w in words.split('\t'):
            #print(w)
            if (i == 0):
                time.append(float(w)/60)
            if (i == 1):
                try:
                    first.append(float(w)/0.000006)
                except:
                    first.append(-7)
            if (i == 2):
                try:
                    second.append(float(w)/0.000006)
                except:
                    second.append(-7)
            i = i + 1

dataFig = {'x': time, 'y': first, 'y2': second}




# BESSEL

data = generate_data()

bes = figure(width = 1100, x_axis_label = 'Modulacja fazowa [rad]', y_axis_label = 'Wydajność dyfrakcyjna [%]')

g1 = bes.line('xB', 'yB1', source = data)
g2 = bes.line('xB', 'yB2', source = data, color = 'red')

bes.toolbar.logo = None
bes.toolbar.autohide = True
bes.grid.grid_line_dash = (6, 5)

#show(bes)


# SLIDER
slider = Slider(start = 1, end = 50, step = 1, value = width, title = 'Width of Bessel', width = 300)
slider.on_change('value_throttled', callback)



fig = figure(width = 1100, x_range = (0, 130), x_axis_label = 'Czas [min]', y_range = (0, 23), y_axis_label = 'Wydajność dyfrakcyjna [%]', sizing_mode = 'stretch_width', height = 300)

fig.circle('x', 'y', source = dataFig)
fig.circle('x', 'y2', source = dataFig, color = 'red')

fig.toolbar.logo = None
fig.toolbar.autohide = True
fig.grid.grid_line_dash = (6, 5)




sh = column(fig, slider, bes)
curdoc().add_root(sh)

