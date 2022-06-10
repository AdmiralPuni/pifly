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