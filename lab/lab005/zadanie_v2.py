from bokeh.core.enums import AutosizeMode, Orientation, VerticalAlign
from bokeh.plotting import figure, show, row, column
from bokeh.io import curdoc
from bokeh.palettes import all_palettes
from bokeh.models import Slider
from bokeh.models import LinearAxis, Range1d

import numpy as np
import scipy.special as sp

time = []
first = []
second = []

width = 15

def generate_data():
    b = np.linspace(0, width, 500)

    v = 1
    bessel1 = sp.jv(v, b/2) * sp.jv(v, b/2) * 100

    v = 2
    bessel2 = sp.jv(v, b/2) * sp.jv(v, b/2) * 100

    data = {'xB': b, 'yB1': bessel1, 'yB2': bessel2}
    return data


def callback(attr, old, new):
    global width
    width = slider.value

    data = generate_data()

    g1.data_source.data = data
    bes.x_range.update(end = width)



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

bes = figure(width = 1100, x_axis_label = 'Modulacja fazowa [rad]', y_axis_label = 'Wydajność dyfrakcyjna [%]', y_range = (0, 30), x_range = (0, width))

g1 = bes.line('xB', 'yB1', source = data)
g2 = bes.line('xB', 'yB2', source = data, color = 'red')

bes.toolbar.logo = None
bes.toolbar.autohide = True
bes.grid.grid_line_dash = (6, 5)



# SLIDER
slider = Slider(start = 1, end = 50, step = 1, value = width, title = 'Width of Bessel', width = 300)
slider.on_change('value_throttled', callback)



bes.extra_x_ranges['foo'] = Range1d(0, 130)
bes.circle('x', 'y', source = dataFig, color = 'navy', x_range_name="foo")
bes.circle('x', 'y2', source = dataFig, color = 'crimson', x_range_name="foo")

ax2 = LinearAxis(x_range_name="foo", axis_label="Czas [min]")
ax2.axis_label_text_color ="navy"
bes.add_layout(ax2, 'above')



sh = column(slider, bes)
curdoc().add_root(sh)

