#!/usr/bin/python3
"""
script starts Flask web app
"""
from flask import Flask
from flask import render_template
from models import storage

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


@app.route("/number_template/<int:n>")
def number_template(n):
    """
    display a HTML page only if n is an integer
    H1 tag: “Number: n” inside the tag BODY
    """
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>")
def odd_even(n):
    """
    display a HTML page only if n is an integer
    H1 tag: “Number: n is even|odd” inside the tag BODY
    """
    number = "even" if (n % 2 == 0) else "odd"
    return render_template("6-number_odd_or_even.html", n=n, number=number)


@app.teardown_appcontext
def tear_down():
    """
    removes the current SQLAlchemy Session after each request
    calls storage.close()
    """
    storage.close()


@app.route("/states")
@app.route("/states_list")
def states_list():
    """
    Displays HTML page with States
    and a list of State objects in DBStorage
    """
    states = storage.all(classes["State"]).values()
    return render_template("7-states_list.html", states=states)


@app.route("/cities_by_states")
def cities_by_states():
    """Displays states with city list"""
    states = storage.all(classes["State"]).values()
    return (render_template('8-cities_by_states.html', states=states))


@app.route('/states/<id>')
def html_if_stateID(id):
    """display html page; customize heading with state.name
       fetch sorted cities for this state ID into LI tag ->in HTML file
    """
    states = None
    for state in storage.all("State").values():
        if state.id == id:
            states = state
    return render_template('9-states.html', states=states)

@app.route('/hbnb_filters')
def html_filters():
    """display html page with working city/state filters & amenities
       runs with web static css files
    """
    states = [s for s in storage.all("State").values()]
    amenity_objs = [a for a in storage.all("Amenity").values()]
    return render_template('10-hbnb_filters.html',
                           states=states, amenity_objs=amenity_objs)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
