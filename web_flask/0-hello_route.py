#!/usr/bin/python3
"""A script that starts a Flask web app
    Must be listening on 0.0.0.0, port 5000
"""
from flask import Flask

app = Flask("__name__")


@app.route("/", strict_slashes=False)
def hello():
    """ Function returns a string """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)