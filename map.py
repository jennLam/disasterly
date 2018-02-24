from plotly.offline import plot
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime


def choropleth_map(locations_lst, z_lst):

    scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],
           [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

    data = [dict(
            type='choropleth',
            colorscale=scl,
            autocolorscale=False,
            locations=locations_lst,
            z=z_lst,
            locationmode='USA-states',
            stream=dict(
                maxpoints=10000
                ),
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )),
            colorbar=dict(
                title="Number of Disasters",
                thickness=15)
            )]

    layout = dict(
        title='Disaster Data',
        margin=dict(
            l=0,
            r=5,
            b=20,
            t=45,
            pad=2
        ),

        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'),
        )

    fig = dict(data=data, layout=layout)

    plot_div = plot(fig, output_type="div")

    return plot_div


def bar_graph(x_lst, y_lst):
    trace = go.Bar(
        x=x_lst,
        y=y_lst,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    data = [trace]
    layout = go.Layout(
        title='Disaster Incident Types',
        # margin= dict(
        #     l=40,
        #     r=15,
        #     b=140,
        #     t=50,
        #     pad=2
        # )
    )

    fig = go.Figure(data=data, layout=layout)

    plot_div = plot(fig, output_type="div")

    return plot_div


def line_graph(x_lst, y_lst):

    trace = go.Scatter(
        x=x_lst,
        y=y_lst,
        name='Time',
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=4,
            dash='dot')
    )

    data = [trace]

    # Edit the layout
    layout = dict(title='Disaster by Time',
                  xaxis=dict(title='Time'),
                  yaxis=dict(title='Number of Disasters'),
                  )

    fig = dict(data=data, layout=layout)
    plot_div = plot(fig, output_type="div")

    return plot_div
