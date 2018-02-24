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
    incident_plot_div = map.bar_graph(incident_results.keys(), incident_results.values())
    time_plot_div = map.line_graph(time_results.keys(), time_results.values())

    return render_template("index.html", incidents=dd.get_categories("incidentType"),
                           hello=Markup(us_plot_div), incident_map=Markup(incident_plot_div),
                           time_map=Markup(time_plot_div))

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")
