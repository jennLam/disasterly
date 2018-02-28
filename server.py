from flask import Flask, render_template, jsonify, request, Markup
from jinja2 import StrictUndefined
import os
from data import DisasterData
from visual import Visual


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

app.jinja_env.undefined = StrictUndefined

dd = DisasterData()


@app.route("/")
def index():
    """Homepage."""

    results_dict = dd.disaster_dict()

    visual = Visual(results_dict)

    visual_dict = visual.create("state", "incident", "date")

    us_plot_div = visual_dict["us_plot_div"]
    incident_plot_div = visual_dict["incident_plot_div"]
    time_plot_div = visual_dict["time_plot_div"]

    return render_template("index.html", states=dd.get_categories("state"), incidents=dd.get_categories("incidentType"),
                           us_map=Markup(us_plot_div), incident_map=Markup(incident_plot_div),
                           time_map=Markup(time_plot_div), states_counties=results_dict["state_county"])


@app.route("/search")
def get_search_results():
    """Get search results."""

    state = request.args.get("state")
    incident = request.args.get("incident")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    results_dict = dd.disaster_dict(state=state, incident_type=incident,
                                    start_date=start_date, end_date=end_date)

    visual = Visual(results_dict)

    visual_dict = visual.create("state", "incident", "date")

    us_plot_div = visual_dict["us_plot_div"]
    incident_plot_div = visual_dict["incident_plot_div"]
    time_plot_div = visual_dict["time_plot_div"]

    return render_template("index.html", states=dd.get_categories("state"), incidents=dd.get_categories("incidentType"),
                           us_map=Markup(us_plot_div), incident_map=Markup(incident_plot_div),
                           time_map=Markup(time_plot_div), states_counties=results_dict["state_county"])

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
