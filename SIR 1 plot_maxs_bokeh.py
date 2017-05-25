# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 24/5/2017
# Plotting Multiple Simulations of a SIR Epidemic Model
# Based on the US unemployment example on Bokeh Website:
#   http://bokeh.pydata.org/en/latest/docs/gallery/unemployment.html


import pandas as pd
from math import pi
from bokeh.io import show, save
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    FixedTicker,
    ColorBar,
)
from bokeh.plotting import figure
import bokeh.palettes as palet

#Choosing the values for c and r to study
cvalues = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]#  
rvalues = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]#

#Lets open our previously generated maxima csv file
maxs = pd.read_csv('infection maxima.csv', index_col = 0)
print(maxs) #to check it

# reshape to 1D array
df = pd.DataFrame(maxs.stack(), columns=['Infected']).reset_index()

print(df) #lets se how it looks like

df.round(1) #making sure there's no weird huge numbers

#preparing the colors to be used
colors = palet.magma(128)
mapper = LinearColorMapper(palette=colors, 
                           low=df.Infected.min(), high=df.Infected.max())

#and define our data as the source for the bokeh plot
source = ColumnDataSource(df)

#more tools can be added here
TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

#starting the whole 'window'
p = figure(title="Infected Maxima for a SIR Epidemic Model",
           x_axis_label = 'Removal Rate', y_axis_label = 'Contagion Rate',
           x_axis_location="above", plot_width=1024, plot_height=1024,
           tools=TOOLS, toolbar_location='below')

#further customization of it
p.title.text_font_size= "30pt"
p.axis.axis_label_text_font_size= "20pt"
p.axis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 3
p.xaxis[0].ticker=FixedTicker(ticks=cvalues)
p.yaxis[0].ticker=FixedTicker(ticks=cvalues)
p.xaxis.major_label_orientation = pi / 2

#now deciding on the gliphs to represent our data, 
#circles are simpler and avoid trouble
p.circle(x="level_0", y="level_1", size=10,
       source=source,
       fill_color={'field': 'Infected', 'transform': mapper},
       line_color=None)

#puting a colorbar next to it, to interpret our colors
color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="7pt",
                     ticker=BasicTicker(desired_num_ticks=10),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

#and whenever we hover the mouse over a data point we get the info on it
p.select_one(HoverTool).tooltips = [
     ('removal | contagion', '@level_0{1.111} |  @level_1{1.111}'),
     ('Infected', '@Infected{1.1}'),
]

#Show the plot, save it, or both
show(p) 
save(p, filename = 'SIR_bokeh_interactive_plot.html', title = 'SIR Epidemic Plot')     
