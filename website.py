import flask
import json
import sql
import paho.mqtt.client as mqtt

def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

client = mqtt.Client()

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

@APP.route('/device/interval', methods=['POST'])
def set_interval():
  device_id = flask.request.form['id']
  interval = flask.request.form['interval']
  sql.update_field('interval', interval, device_id)
  client.connect("192.168.43.109", 1883, 60)
  publish(client, device_id, interval)
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