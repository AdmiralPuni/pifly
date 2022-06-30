from flask import render_template, redirect, url_for, request, abort, Blueprint
from controllers.utils import utils as controller_utils

blueprint = Blueprint('user_pages', __name__)

@blueprint.route('/my/dashboard', methods=['GET'])
def index():
  controller_utils.check_session()
  return render_template('user/dashboard.html')

@blueprint.route('/my/profile', methods=['GET'])
def profile():
  controller_utils.check_session()
  return render_template('user/profile.html')

@blueprint.route('/my/devices', methods=['GET'])
def devices():
  controller_utils.check_session()
  return render_template('user/devices.html')

@blueprint.route('/my/help', methods=['GET'])
def help():
  controller_utils.check_session()
  return render_template('user/help.html')

@blueprint.route('/my/about', methods=['GET'])
def about():
  controller_utils.check_session()
  return render_template('user/about.html')

@blueprint.route('/my/settings', methods=['GET'])
def settings():
  controller_utils.check_session()
  return render_template('user/settings.html')