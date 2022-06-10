from flask import render_template, redirect, url_for, request, abort, Blueprint

blueprint = Blueprint('user_pages', __name__)

@blueprint.route('/my/dashboard', methods=['GET'])
def index():
  return render_template('user/dashboard.html')