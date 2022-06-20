from flask import render_template, redirect, url_for, request, abort, Blueprint

blueprint = Blueprint('pages', __name__)

@blueprint.route('/', methods=['GET'])
def index():
  return render_template('auth.html')

@blueprint.route('/auth', methods=['GET'])
def auth():
  return render_template('auth.html')

@blueprint.route('/register', methods=['GET'])
def register():
  return render_template('register.html')