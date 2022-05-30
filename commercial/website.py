import flask
import json
import database as db
import datetime

# Create the application.
APP = flask.Flask(__name__)

# Create a URL route in our application for "/"
@APP.route('/')
def home():
  return flask.render_template('index.html')

if __name__ == '__main__':
  APP.run(debug=True, host="0.0.0.0")