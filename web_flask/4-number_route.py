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


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Function returns a string """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def cText(text):
    """ display “C ” followed by the value of the text variable """
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def isCool(text="is cool"):
    """ display “Python” followed by the value of the text variable """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """display number only if n is an int"""
    if isinstance(n, int):
        return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
