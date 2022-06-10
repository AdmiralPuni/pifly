import flask
from models.utils import utils
from models.device import device

blueprint = flask.Blueprint('api_device', __name__)

@blueprint.route('/api/device/get', methods=['GET'])
def index():
  return 'Hello, World!'

@blueprint.route('/api/device/add', methods=['POST'])
def add():
  data = {
    'name': flask.request.form['name'],
    'serial_number': flask.request.form['serial_number'],
    'user_id': flask.session['user_id'],
    'interval': 30
  }

  for key in data:
    if data[key] == '':
      return utils.reply('error', 'GIE-1', 'Missing parameter: ' + key)

  if device.insert(data):
    return utils.reply('success', 'GIS-0', 'Device added')
  else:
    return utils.reply('error', 'GIE-1', 'Error adding device')
  
@blueprint.route('/api/device/my', methods=['GET'])
def my():
  user_id = flask.session['user_id']
  devices = device.user_devices(user_id)
  return flask.jsonify({'status': 'success', 'devices': devices})

@blueprint.route('/api/device/delete', methods=['POST'])
def delete():
  serial_number = flask.request.form['serial_number']
  user_id = flask.session['user_id']
  if device.delete(serial_number, user_id):
    return utils.reply('success', 'GID-0', 'Device deleted')
  else:
    return utils.reply('error', 'GIE-1', 'Error deleting device')
  

@blueprint.route('/api/device/update', methods=['POST'])
def update():
  data = {
    'serial_number': flask.request.form['serial_number'],
    'name': flask.request.form['name']
  }

  for key in data:
    if data[key] == '':
      return utils.reply('error', 'GIE-1', 'Missing parameter: ' + key)

  if device.update_by_serial_number(data):
    return utils.reply('success', 'GIE-0', 'Device updated')
  else:
    return utils.reply('error', 'GIE-1', 'Error updating device')

#interval update
@blueprint.route('/api/device/update/interval', methods=['POST'])
def update_interval():
  data = {
    'serial_number': flask.request.form['serial_number'],
    'interval': flask.request.form['interval']
  }

  for key in data:
    if data[key] == '':
      return utils.reply('error', 'GIE-1', 'Missing parameter: ' + key)

  if device.update_by_serial_number(data):
    return utils.reply('success', 'GIE-0', 'Device updated')
  else:
    return utils.reply('error', 'GIE-1', 'Error updating device')