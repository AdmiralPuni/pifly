from flask import render_template, redirect, url_for, request, abort, Blueprint, jsonify
import os

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

@blueprint.route('/exp', methods=['GET'])
def exp():
  return render_template('exp.html')

@blueprint.route('/exp/list', methods=['GET'])
def exp_list():
  #return files in static/experiment
  files = os.listdir('static/experiment')
  return jsonify(files)