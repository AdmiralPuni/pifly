from flask import render_template, redirect, url_for, request, abort, Blueprint

blueprint = Blueprint('user_pages', __name__)

@blueprint.route('/my/dashboard', methods=['GET'])
def index():
  return render_template('user/dashboard.html')

@blueprint.route('/my/profile', methods=['GET'])
def profile():
  return render_template('user/profile.html')

@blueprint.route('/my/devices', methods=['GET'])
def devices():
  return render_template('user/devices.html')

@blueprint.route('/my/help', methods=['GET'])
def help():
  return render_template('user/help.html')