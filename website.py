import flask
import json
import sql

# Create the application.
APP = flask.Flask(__name__)

# Create a URL route in our application for "/"
@APP.route('/')
def home():
  return flask.render_template('index.html')

@APP.route('/stats')
def stats():
  return flask.render_template('stats.html')

@APP.route('/devices')
def coindata():
  data = sql.select_device_id()
  return json.dumps(data)

@APP.route('/device/add', methods=['POST'])
def add_device():
  data = flask.request.form['device-id']
  sql.insert_new_device(data)
  return 'OK'

@APP.route('/device/remove', methods=['GET'])
def remove_device():
  data = flask.request.args['id']
  sql.delete_device(data)
  return 'OK'

@APP.route('/data')
def data():
  data = sql.select_all_device()
  return json.dumps(data)

if __name__ == '__main__':
  APP.run(debug=True, host="0.0.0.0")