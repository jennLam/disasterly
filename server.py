from flask import Flask, render_template, jsonify, request
from jinja2 import StrictUndefined
import os
from data import DisasterData


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

app.jinja_env.undefined = StrictUndefined

dd = DisasterData()


@app.route("/")
def index():
    """Homepage."""
    return render_template("index.html", incidents=dd.get_categories("incidentType"))


@app.route("/search.json")
def get_search_results():
    """Get search results."""

    incident = request.args.get("incident")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    print incident
    print start_date
    print end_date

    adv_search_results = dd.advanced_search(incident_type=incident,
                                            start_date=start_date, end_date=end_date)

    results = dd.create_disaster_dict(adv_search_results)

    # print results

    return jsonify(results)

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")
