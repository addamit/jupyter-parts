#http://holoviews.org/user_guide/Deploying_Bokeh_Apps.html
import numpy as np
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from bokeh.layouts import layout
from bokeh.io import curdoc

from bokeh.models import Panel, Tabs
from bokeh.layouts import row


from bokeh.sampledata.les_mis import data


n = 1000
x = 3 + 3*np.random.standard_normal(n)
y = 3 + 3*np.random.standard_normal(n)

p1 = figure(background_fill_color='white', match_aspect=True,)
p1.scatter(x, y, size=3, color="black")
tab1 = Panel(child=p1, title="Scatter Plot")
p1.grid.visible = False

p2 = figure(background_fill_color='white', match_aspect=True,)
p2.hexbin(x,y, size=0.3, hover_alpha=0.5,line_color='grey')
tab2 = Panel(child=p2, title="Hexbin Plot")
p2.grid.visible = False

mytabs=[ tab1, tab2 ]


start, end = 1, 20
samples_count = 5
slider = Slider(start=start, end=end, value=start, step=1, title="Counts")
select = Select(title="Count", value="aux", options=["box", "pack", "image", "user"])

renderer = hv.renderer('bokeh')##.instance(mode='server')
hv.extension('bokeh')
hv.output(size=200)
links = pd.DataFrame(data['links'])
print(links.head(3))

def mychart(dummy_df):
	print ("num: {}".format(len(dummy_df)))
	nodes = hv.Dataset(pd.DataFrame(data['nodes']), 'index')
	chord = hv.Chord((links, nodes)).select(value=(5, None))
	chord.opts(opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(), labels='name', node_color=dim('index').str()))    	
	# Create HoloViews plot and attach the document
	hvplot = renderer.get_plot(chord)
	return hvplot

dummy_df = pd.DataFrame({'x' : [1,2,3], 'y' : [4,5,6]})
stream = hv.streams.Pipe(dummy_df=dummy_df)
dmap1 = hv.DynamicMap(mychart, streams=[stream])
# dmap1 = hv.DynamicMap(mychart, kdims='num').redim.range(num=(1,10))
# widget0 = renderer.get_widget(dmap1, None, position='above')
widget1 = renderer.get_plot(dmap1, None, position='above').state

tab3 = Panel(child=row( widget1), title="Chord Plot")

mytabs.append(tab3)
views = Tabs(tabs = mytabs)
layout=row(views)
curdoc().add_root(layout)

