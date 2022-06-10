from flask import *

from controllers.pages import blueprint as pages_blueprint
from controllers.auth import blueprint as auth_blueprint

from controllers.user.pages import blueprint as user_pages_blueprint

from controllers.api.device import blueprint as api_device_blueprint
from controllers.api.user import blueprint as api_user_blueprint

APP = Flask(__name__)
APP.secret_key = 'DvS}4F/DE44nNK)shuZpB5.TEM~tYn'

APP.register_blueprint(pages_blueprint)
APP.register_blueprint(auth_blueprint)

APP.register_blueprint(user_pages_blueprint)

APP.register_blueprint(api_device_blueprint)
APP.register_blueprint(api_user_blueprint)

if __name__ == '__main__':
  APP.run(debug=True, host="0.0.0.0", threaded=True)
  
