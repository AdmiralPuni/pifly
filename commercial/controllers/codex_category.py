from flask import render_template, redirect, url_for, request, abort, jsonify, Blueprint
from models.codex_category import codex_category
import time

blueprint = Blueprint('codex_category', __name__)


@blueprint.route('/api/category/get', methods=['GET'])
def get():
  #get name from get request
  name = request.args.get('name')
  #get codex_category from database
  print(name)
  result = codex_category.find(name)
  #append timestamp to result
  result["timestamp"] = time.time()

  return jsonify(result)

@blueprint.route('/api/category/get/all', methods=['GET'])
def get_all():
  result = codex_category.get_all()
  data = {
    "status": "success",
    "timestamp": time.time(),
    "body": result
  }

  return jsonify(data)
