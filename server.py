from flask import Flask, render_template, jsonify, request, Markup
from jinja2 import StrictUndefined
import os
from data import DisasterData
import visual


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

    results_dict = dd.make_dict(adv_search_results)

    us_plot_div = visual.choropleth_map(results_dict["state"].keys(), results_dict["state"].values())
    incident_plot_div = visual.bar_graph(results_dict["incident"].keys(), results_dict["incident"].values())
    time_plot_div = visual.line_graph(results_dict["date"].keys(), results_dict["date"].values())

    return render_template("index.html", incidents=dd.get_categories("incidentType"),
                           hello=Markup(us_plot_div), incident_map=Markup(incident_plot_div),
                           time_map=Markup(time_plot_div), counties=results_dict["state_county"])

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")
