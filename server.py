from flask import Flask, render_template, jsonify, request, Markup
from jinja2 import StrictUndefined
import os
from plotly.offline import plot
from data import DisasterData

import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

app.jinja_env.undefined = StrictUndefined

dd = DisasterData()






@app.route("/")
def index():
    """Homepage."""
    return render_template("index.html", incidents=dd.get_categories("incidentType"), hello="hi")


@app.route("/search")
def get_search_results():
    """Get search results."""

    incident = request.args.get("incident")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # print incident
    # blah_date = datetime.strptime(start_date, "%Y-%m-%d")
    # print end_date
    # print type(blah_date)


    adv_search_results = dd.advanced_search(incident_type=incident,
                                            start_date=start_date, end_date=end_date)

    state_results = dd.create_disaster_dict3(adv_search_results, "state")
    incident_results = dd.create_disaster_dict3(adv_search_results, "incidentType") 

    
    scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

    adv_search_results['text'] = adv_search_results['state'] + '<br>' +\
    'Incident '+adv_search_results['incidentType'] + "<br>" + \
    "Country "

    adv_search_results["count"] = 1
    # print adv_search_results

    data = [ dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = False,
            locations = state_results.keys(),
            z = state_results.values(),
            locationmode = 'USA-states',
            stream = dict (
                maxpoints = 10000
                ),
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                ) ),
            colorbar = dict(
                title = "Millions USD",
                thickness=20)
            ) ]

    layout = dict(
            title = 'Disaster Data',

            margin= dict(
            l=0,
            r=5,
            b=20,
            t=45,
            pad=2
        ),

            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)'),
                 )
        
    fig = dict( data=data, layout=layout )
    # blah = py.iplot( fig, filename='d3-cloropleth-map' )
    plot_div = plot(fig, output_type="div")








    trace0 = go.Bar(
        x=incident_results.keys(),
        y=incident_results.values(),
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    data2 = [trace0]
    layout2 = go.Layout(
        title='Disaster Incident Types',
        margin= dict(
            l=40,
            r=15,
            b=140,
            t=50,
            pad=2
        )
    )

    fig2 = go.Figure(data=data2, layout=layout2)
    # py.iplot(fig, filename='text-hover-bar')
    plot_div2 = plot(fig2, output_type="div")



    return render_template("index.html", incidents=dd.get_categories("incidentType"),
                           hello=Markup(plot_div), incident_map=Markup(plot_div2))

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")
