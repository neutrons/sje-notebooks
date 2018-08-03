# coding: utf-8

import os, numpy as np
datadir = os.path.expanduser('~/notebooks/ARCS')


import pandas as pd
import numpy as np
import scipy as sp
import plotly, plotly.plotly as py, plotly.figure_factory as ff, plotly.graph_objs as go

from ipywidgets import widgets
from IPython.display import display, clear_output, Image
from plotly.widgets import GraphWidget


# initialize plotly
plotly.tools.set_credentials_file(username='mcvine', api_key='xPhu0GyBCi4iiEI3unYE')


def createIntResPlot():
    # read data
    print "reading data. please wait..."
    vdata = pd.read_csv(os.path.join(datadir, './V_Cali_Int_Res_FC1_2018.dat'), delimiter=' ')
    vtable = ff.create_table(vdata)
    print "  done"
    choppers = np.array(vdata.Chopper, dtype=int)
    chopper_freqs = np.array([getattr(vdata, "Chopper%d"%c)[i] for i, c in enumerate(choppers)])
    intensity = vdata.Height * vdata.Sigma
    resolution = vdata.Sigma
    Ei_list = list(vdata.Energy.unique())


    # Plotting widget
    print "preparing widget..."
    g = GraphWidget('https://plot.ly/~mcvine/2')

    # Dropdown list
    Ei_str_list = map(str, Ei_list)
    initial_Ei = 100.
    Ei_select = widgets.Dropdown(
        options=Ei_str_list,
        value=str(initial_Ei),
        description='Incident energy',
    )

    def on_Ei_change(_):
        Ei = float(Ei_select.value)
        condition = np.isclose(vdata.Energy, Ei)
        labels = ['Chopper %s. Freq: %s' % (c, f) 
                  for c,f in zip(choppers[condition], chopper_freqs[condition])]
        trace = go.Scatter(
            x = resolution[condition],
            y = vdata.Height[condition],
            mode = 'markers+text',
            text = labels,
            textposition='top center'
        )
        data = [trace]
        layout = go.Layout(
            title = 'Flux (peak height) vs elastic resolution (peak width). Ei=%s meV' % Ei,
            showlegend=False,
            xaxis=dict(
                title='Resolution (meV)',
            ),
            yaxis=dict(
                title='Flux (arb. unit)',
            )
        )
        fig = go.Figure(data=data, layout=layout)
        g.plot(fig)

    Ei_select.observe(on_Ei_change)
    print "  done"
    return widgets.VBox([Ei_select, g])
