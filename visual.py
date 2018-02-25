from plotly.offline import plot
import plotly.graph_objs as go
from random import randint


def choropleth_map(locations_lst, z_lst):

    scl = [[0.0, 'rgb(255,236,210)'], [1.0, 'rgb(223,100,87)']]

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
                titlefont=dict(
                    family='Lato',
                    size=12
                    ),
                tickfont=dict(
                    family='Lato',
                    size=12
                    ),
                bordercolor="rgb(255,255,255)",
                thickness=15)
            )]

    layout = dict(
        # title='Disaster Data',
        margin=dict(
            l=0,
            r=5,
            b=20,
            t=15,
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

    scl = ['rgb(255,166,48)', 'rgb(255,236,210)', 'rgb(223,100,87)', 'rgb(245,121,66)', 'rgb(252,193,116)']

    rand_cl = []

    for i in range(len(x_lst)):
        rand_cl.append(scl[randint(0, 4)])

    trace = go.Bar(
        x=x_lst,
        y=y_lst,
        marker=dict(
            color=rand_cl,
            line=dict(
                color='rgb(255,255,255)',
                width=1.5,
            )
        ),
        opacity=1.0
    )

    data = [trace]
    layout = go.Layout(
        # title='Disaster Incident Types',
        font=dict(family='Lato', size=12, color='#000000'),
        margin=dict(
            l=45,
            r=20,
            b=135,
            t=20,
            pad=2
        )
    )

    fig = go.Figure(data=data, layout=layout)

    plot_div = plot(fig, output_type="div")

    return plot_div


def line_graph(x_lst, y_lst):

    scl = ['rgb(255,166,48)', 'rgb(223,100,87)', 'rgb(245,121,66)', 'rgb(252,193,116)']

    trace = go.Scatter(
        x=x_lst,
        y=y_lst,
        name='Time',
        line=dict(
            color=scl[randint(0, 3)],
            width=4,
            dash='dot')
    )

    data = [trace]

    # Edit the layout
    # title='Disaster by Time',
    layout = dict(
        # xaxis=dict(title='Time'),
        # yaxis=dict(title='Number of Disasters'),
        font=dict(family='Lato', size=12, color='#000000'),
        margin=dict(
            l=45,
            r=20,
            b=40,
            t=20,
            pad=2
            ))

    fig = dict(data=data, layout=layout)
    plot_div = plot(fig, output_type="div")

    return plot_div
