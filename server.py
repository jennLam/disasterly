from flask import Flask, render_template, jsonify, request
from jinja2 import StrictUndefined
import os


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""
    return render_template("index.html")


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")