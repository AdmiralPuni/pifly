import flask
from models.utils import utils
from models.user import user

blueprint = flask.Blueprint('api_user', __name__)

@blueprint.route('/api/user/get', methods=['GET'])
def get():
  user_id = flask.session['user_id']

  user_data = user.single(user_id)
  if user_data is not None:
    return flask.jsonify({'status': 'success', 'code': 'AU-1', 'data': user_data})
  else:
    return utils.reply('error', 'AU-2', 'User not found')

@blueprint.route('/api/user/update/data', methods=['POST'])
def update():
  data = {
    'id': flask.session['user_id'],
    'name': flask.request.form['name'],
    'email': flask.request.form['email'],
    'phone': flask.request.form['phone']
  }

  for key in data:
    if data[key] == '':
      return utils.reply('error', 'AU-3', 'Please fill all fields')

  if user.update(data):
    flask.session['username'] = data['name']
    return utils.reply('success', 'AU-3', 'User updated')
  else:
    return utils.reply('error', 'AU-4', 'User not updated')

@blueprint.route('/api/user/update/password', methods=['POST'])
def update_password():
  data = {
    'id': flask.session['user_id'],
    'old_password': flask.request.form['old_password'],
    'new_password': flask.request.form['new_password']
  }

  for key in data:
    if data[key] == '':
      return utils.reply('error', 'AU-5', 'Please fill all fields')

  if user.verify_password(data['id'], data['old_password']):
    if user.update({'id': data['id'], 'password': utils.hash(data['new_password'])}):
      return utils.reply('success', 'AU-5', 'Password updated')
    else:
      return utils.reply('error', 'AU-6', 'Password not updated')
  else:
    return utils.reply('error', 'AU-7', 'Old password is incorrect')