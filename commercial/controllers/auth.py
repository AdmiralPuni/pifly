import flask
from models.user import user
from models.utils import utils
from controllers.utils import utils as controller_utils

blueprint = flask.Blueprint('auth_blueprint', __name__)

@blueprint.route('/auth/verify', methods=['POST'])
def verify():
  #get username and password from post request
  email = flask.request.form['email']
  password = flask.request.form['password']

  #check if both username and password are not empty
  if email == '' or password == '':
    return flask.abort(400)

  result = user.verify(email, password)
  if result is not False:
    print(result)
    #set session variables
    flask.session['username'] = result[1]
    flask.session['user_id'] = result[0]
    flask.session['logged_in'] = True

    return utils.reply("success", "FUIS-1", "Login successful")
  else:
    return utils.reply("error", "GIE-1", "Invalid username or password")

@blueprint.route('/auth/register', methods=['POST'])
def register():
  #get username and password from post request
  data = {
    'name': flask.request.form['name'],
    'email': flask.request.form['email'],
    'password': flask.request.form['password'],
    'phone': flask.request.form['phone'],
    'level': 10
  }

  #if flask.request.form['code'] != '':
  #  return utils.reply("error", "GIE-2", "Invalid code")

  for key in data:
    if data[key] == '':
      return utils.reply("error", "GIE-1", "Missing data")

  result = user.insert(data)
  if result is True:
    return utils.reply("success", "FUIS-1", "Registration successful")
  else:
    return utils.reply("error", "GIE-1", "Registration failed")

@blueprint.route('/auth/logout', methods=['GET'])
def logout():
  #clear session variables
  flask.session.clear()

  #redirect to /
  return flask.redirect(flask.url_for('pages.index'))

@blueprint.route('/user/data', methods=['GET'])
def get_user_data():
  controller_utils.check_session()
  data = {
    'id': flask.session['user_id'],
    'name': flask.session['username']
  }

  return flask.jsonify(data)