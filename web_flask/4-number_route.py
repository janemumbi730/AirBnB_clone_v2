#!/usr/bin/python3
"""
Module 4-number_route.Starts a Flask Web App
"""
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello_hbnb():
    """
    route function
    displays the string on url page
    """
    return ("Hello HBNB!")


@app.route("/hbnb")
def hbnb():
    """
    displays HBNB when /hbnb is used in url
    """
    return ("HBNB!")


@app.route("/c/<text>")
def c_is_fun(text):
    """
    Dispays C followed by value in <text>
    Without the text it returns 404
    """
    return ("C {}".format(text.replace('_', ' ')))


@app.route("/python")
@app.route("/python/<text>")
def python_is_cool(text="is cool"):
    """
    display “Python ”, followed by the value of the text variable
    replaces underscore _ symbols with a space
    The default value of text is “is cool”
    """
    return ("Python {}".format(text.replace('_', ' ')))


@app.route("/number/<int:n>")
def is_number(n):
    """display text only if int given"""
    return ("{} is a number".format(n))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
