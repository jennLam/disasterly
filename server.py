from flask import Flask, render_template, jsonify, request, Markup
from jinja2 import StrictUndefined
import os
from plotly.offline import plot
from data import DisasterData

import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
import map


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

app.jinja_env.undefined = StrictUndefined

dd = DisasterData()



@app.route("/")
def index():
    """Homepage."""
    return render_template("index.html", incidents=dd.get_categories("incidentType"),
                           hello="hi", incident_map="hi", time_map="hi")


@app.route("/search")
def get_search_results():
    """Get search results."""

    incident = request.args.get("incident")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    adv_search_results = dd.advanced_search(incident_type=incident,
                                            start_date=start_date, end_date=end_date)

    state_results = dd.create_disaster_dict3(adv_search_results, "state")
    incident_results = dd.create_disaster_dict3(adv_search_results, "incidentType")
    time_results = dd.disaster_dict_timeline_dict(adv_search_results)
    county_results = dd.create_disaster_dict3(adv_search_results, "declaredCountyArea")

    us_plot_div = map.choropleth_map(state_results.keys(), state_results.values())


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
        # margin= dict(
        #     l=40,
        #     r=15,
        #     b=140,
        #     t=50,
        #     pad=2
        # )
    )

    fig2 = go.Figure(data=data2, layout=layout2)
    # py.iplot(fig, filename='text-hover-bar')
    plot_div2 = plot(fig2, output_type="div")







    month = time_results.keys()

    high_2007 = time_results.values()



    trace = go.Scatter(
        x = month,
        y = high_2007,
        name = 'High 2007',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4,
            dash = 'dot') # dash options include 'dash', 'dot', and 'dashdot'
    )

    data3 = [trace]

    # Edit the layout
    layout3 = dict(title = 'Disaster by Time',
                  xaxis = dict(title = 'Time'),
                  yaxis = dict(title = 'Number of Disasters'),
                  )

    fig3 = dict(data=data3, layout=layout3)
    plot_div3 = plot(fig3, output_type="div")





    return render_template("index.html", incidents=dd.get_categories("incidentType"),
                           hello=Markup(us_plot_div), incident_map=Markup(plot_div2),
                           time_map=Markup(plot_div3))

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")
